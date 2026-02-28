from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.auth import current_user
from app.db import get_db
from app.models import Attachment, Project, Severity, Ticket, TicketType, User
from app.schemas import CommentIn, CommentOut, TicketIn, TicketOut, TicketPatch
from app.sla import should_auto_assign, sla_for_severity
from app.security_uploads import assert_safe_upload, store_bytes
from app.models import Comment

router = APIRouter(tags=["tickets"])


def _ticket_out(t: Ticket) -> TicketOut:
    return TicketOut.model_validate(t)


@router.get("/projects/{project_id}/tickets", response_model=list[TicketOut])
def list_tickets(project_id: int, db: Session = Depends(get_db), _: User = Depends(current_user)):
    if not db.get(Project, project_id):
        raise HTTPException(status_code=404, detail="project not found")
    return (
        db.query(Ticket)
        .filter(Ticket.project_id == project_id)
        .order_by(Ticket.created_at.desc())
        .limit(200)
        .all()
    )


@router.post("/projects/{project_id}/tickets", response_model=TicketOut)
def create_ticket(project_id: int, body: TicketIn, db: Session = Depends(get_db), user: User = Depends(current_user)):
    if not db.get(Project, project_id):
        raise HTTPException(status_code=404, detail="project not found")
    if body.ticket_type == TicketType.bug and body.severity is None:
        raise HTTPException(status_code=400, detail="bugs need severity")
    if body.ticket_type != TicketType.bug and body.severity is not None:
        raise HTTPException(status_code=400, detail="severity only for bugs")

    sla = None
    assignee_id = None
    if body.severity is not None:
        sla = sla_for_severity(body.severity)
        if should_auto_assign(body.severity):
            assignee_id = user.id

    ticket = Ticket(
        project_id=project_id,
        sprint_id=body.sprint_id,
        ticket_type=body.ticket_type,
        status=body.status,
        title=body.title.strip(),
        body=body.body,
        severity=body.severity,
        assignee_id=assignee_id,
        reporter_id=user.id,
        sla_hours=sla,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.get("/tickets/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db), _: User = Depends(current_user)):
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="not found")
    return ticket


@router.patch("/tickets/{ticket_id}", response_model=TicketOut)
def patch_ticket(ticket_id: int, body: TicketPatch, db: Session = Depends(get_db), _: User = Depends(current_user)):
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="not found")
    if body.status is not None:
        ticket.status = body.status
    if body.sprint_id is not None:
        ticket.sprint_id = body.sprint_id
    if body.assignee_id is not None:
        ticket.assignee_id = body.assignee_id
    db.commit()
    db.refresh(ticket)
    return ticket


@router.get("/tickets/{ticket_id}/comments", response_model=list[CommentOut])
def list_comments(ticket_id: int, db: Session = Depends(get_db), _: User = Depends(current_user)):
    if not db.get(Ticket, ticket_id):
        raise HTTPException(status_code=404, detail="not found")
    return db.query(Comment).filter(Comment.ticket_id == ticket_id).order_by(Comment.created_at.asc()).all()


@router.post("/tickets/{ticket_id}/comments", response_model=CommentOut)
def add_comment(ticket_id: int, body: CommentIn, db: Session = Depends(get_db), user: User = Depends(current_user)):
    if not db.get(Ticket, ticket_id):
        raise HTTPException(status_code=404, detail="not found")
    c = Comment(ticket_id=ticket_id, author_id=user.id, body=body.body.strip())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


@router.post("/tickets/{ticket_id}/attachments")
async def upload_attachment(
    ticket_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: User = Depends(current_user),
):
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="not found")
    raw = await file.read()
    assert_safe_upload(file, raw)
    dest = store_bytes(ticket_id, file.filename or "upload.bin", raw)
    att = Attachment(
        ticket_id=ticket_id,
        filename=file.filename or "upload.bin",
        mime=(file.content_type or "application/octet-stream").split(";")[0],
        size_bytes=len(raw),
        stored_as=str(dest),
    )
    db.add(att)
    db.commit()
    return {"id": att.id, "filename": att.filename}
