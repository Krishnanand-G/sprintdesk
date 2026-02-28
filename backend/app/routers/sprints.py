from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import current_user
from app.db import get_db
from app.models import Project, Sprint, Ticket, TicketStatus, User
from app.schemas import BoardSummary, SprintIn, SprintOut

router = APIRouter(prefix="/projects/{project_id}/sprints", tags=["sprints"])


def _project_or_404(db: Session, project_id: int) -> Project:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="project not found")
    return project


@router.get("", response_model=list[SprintOut])
def list_sprints(project_id: int, db: Session = Depends(get_db), _: User = Depends(current_user)):
    _project_or_404(db, project_id)
    return db.query(Sprint).filter(Sprint.project_id == project_id).order_by(Sprint.start_date.desc()).all()


@router.post("", response_model=SprintOut)
def create_sprint(project_id: int, body: SprintIn, db: Session = Depends(get_db), _: User = Depends(current_user)):
    _project_or_404(db, project_id)
    if body.end_date < body.start_date:
        raise HTTPException(status_code=400, detail="end before start")
    sprint = Sprint(project_id=project_id, name=body.name.strip(), start_date=body.start_date, end_date=body.end_date, status=body.status)
    db.add(sprint)
    db.commit()
    db.refresh(sprint)
    return sprint


@router.get("/{sprint_id}/board-summary", response_model=BoardSummary)
def board_summary(project_id: int, sprint_id: int, db: Session = Depends(get_db), _: User = Depends(current_user)):
    _project_or_404(db, project_id)
    sprint = db.get(Sprint, sprint_id)
    if not sprint or sprint.project_id != project_id:
        raise HTTPException(status_code=404, detail="sprint not found")
    counts = {s: 0 for s in TicketStatus}
    rows = (
        db.query(Ticket.status, db.query(Ticket).filter(Ticket.sprint_id == sprint_id).count())
    )
    q = db.query(Ticket).filter(Ticket.sprint_id == sprint_id)
    for t in q.all():
        counts[t.status] += 1
    return BoardSummary(backlog=counts[TicketStatus.backlog], todo=counts[TicketStatus.todo], doing=counts[TicketStatus.doing], done=counts[TicketStatus.done])
