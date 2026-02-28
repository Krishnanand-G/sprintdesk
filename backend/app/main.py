from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import hash_password
from app.config import get_settings
from app.db import Base, SessionLocal, engine
from app.models import Project, User
from app.routers import auth_routes, projects, sprints, tickets


def seed():
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.email == "triager@local.dev").first():
            db.add(
                User(
                    email="triager@local.dev",
                    hashed_password=hash_password("triager123"),
                    display_name="Triager",
                )
            )
            db.commit()
        if not db.query(Project).filter(Project.key == "DESK").first():
            db.add(Project(name="SprintDesk Demo", key="DESK"))
            db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings = get_settings()
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)
    seed()
    yield


app = FastAPI(title="SprintDesk", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_routes.router)
app.include_router(projects.router)
app.include_router(sprints.router)
app.include_router(tickets.router)


@app.get("/health")
def health():
    return {"ok": True}
