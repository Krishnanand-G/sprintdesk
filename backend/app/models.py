import enum
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class TicketType(str, enum.Enum):
    story = "story"
    bug = "bug"
    task = "task"


class TicketStatus(str, enum.Enum):
    backlog = "backlog"
    todo = "todo"
    doing = "doing"
    done = "done"


class Severity(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class SprintStatus(str, enum.Enum):
    planned = "planned"
    active = "active"
    closed = "closed"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    display_name: Mapped[str] = mapped_column(String(120), default="")
    assigned_tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="assignee", foreign_keys="Ticket.assignee_id"
    )
    reported_tickets: Mapped[list["Ticket"]] = relationship(
        foreign_keys="Ticket.reporter_id"
    )
    comments: Mapped[list["Comment"]] = relationship(back_populates="author")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    key: Mapped[str] = mapped_column(String(16), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    sprints: Mapped[list["Sprint"]] = relationship(back_populates="project")
    tickets: Mapped[list["Ticket"]] = relationship(back_populates="project")


class Sprint(Base):
    __tablename__ = "sprints"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    name: Mapped[str] = mapped_column(String(120))
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    status: Mapped[SprintStatus] = mapped_column(Enum(SprintStatus), default=SprintStatus.planned)
    project: Mapped[Project] = relationship(back_populates="sprints")
    tickets: Mapped[list["Ticket"]] = relationship(back_populates="sprint")


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    sprint_id: Mapped[int | None] = mapped_column(ForeignKey("sprints.id"), nullable=True)
    ticket_type: Mapped[TicketType] = mapped_column(Enum(TicketType))
    status: Mapped[TicketStatus] = mapped_column(Enum(TicketStatus), default=TicketStatus.backlog)
    title: Mapped[str] = mapped_column(String(200))
    body: Mapped[str] = mapped_column(Text, default="")
    severity: Mapped[Severity | None] = mapped_column(Enum(Severity), nullable=True)
    assignee_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    reporter_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    sla_hours: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    project: Mapped[Project] = relationship(back_populates="tickets")
    sprint: Mapped[Sprint | None] = relationship(back_populates="tickets")
    assignee: Mapped[User | None] = relationship(
        back_populates="assigned_tickets", foreign_keys=[assignee_id]
    )
    reporter: Mapped[User] = relationship(foreign_keys=[reporter_id])
    comments: Mapped[list["Comment"]] = relationship(back_populates="ticket")
    attachments: Mapped[list["Attachment"]] = relationship(back_populates="ticket")


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ticket: Mapped[Ticket] = relationship(back_populates="comments")
    author: Mapped[User] = relationship(back_populates="comments")


class Attachment(Base):
    __tablename__ = "attachments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"))
    filename: Mapped[str] = mapped_column(String(255))
    mime: Mapped[str] = mapped_column(String(100))
    size_bytes: Mapped[int] = mapped_column(Integer)
    stored_as: Mapped[str] = mapped_column(String(255))
    ticket: Mapped[Ticket] = relationship(back_populates="attachments")
