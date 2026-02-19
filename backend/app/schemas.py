from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field

from app.models import Severity, SprintStatus, TicketStatus, TicketType


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: EmailStr
    display_name: str

    class Config:
        from_attributes = True


class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    display_name: str = ""


class ProjectIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    key: str = Field(min_length=2, max_length=16)


class ProjectOut(BaseModel):
    id: int
    name: str
    key: str
    created_at: datetime

    class Config:
        from_attributes = True


class SprintIn(BaseModel):
    name: str
    start_date: date
    end_date: date
    status: SprintStatus = SprintStatus.planned


class SprintOut(BaseModel):
    id: int
    project_id: int
    name: str
    start_date: date
    end_date: date
    status: SprintStatus

    class Config:
        from_attributes = True


class TicketIn(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    body: str = ""
    ticket_type: TicketType
    status: TicketStatus = TicketStatus.backlog
    sprint_id: int | None = None
    severity: Severity | None = None


class TicketPatch(BaseModel):
    status: TicketStatus | None = None
    sprint_id: int | None = None
    assignee_id: int | None = None


class TicketOut(BaseModel):
    id: int
    project_id: int
    sprint_id: int | None
    ticket_type: TicketType
    status: TicketStatus
    title: str
    body: str
    severity: Severity | None
    assignee_id: int | None
    reporter_id: int
    sla_hours: int | None
    created_at: datetime

    class Config:
        from_attributes = True


class CommentIn(BaseModel):
    body: str = Field(min_length=1)


class CommentOut(BaseModel):
    id: int
    ticket_id: int
    author_id: int
    body: str
    created_at: datetime

    class Config:
        from_attributes = True


class BoardSummary(BaseModel):
    backlog: int
    todo: int
    doing: int
    done: int
