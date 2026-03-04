import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SECRET_KEY"] = "test-secret"
os.environ["UPLOAD_DIR"] = str(Path(__file__).parent / "_uploads")

from app.auth import hash_password, make_token
from app.db import Base, get_db
from app.main import app
from app.models import Project, User


@pytest.fixture()
def db_session(tmp_path, monkeypatch):
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path / "up"))
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)
    session = TestingSession()
    user = User(
        email="triager@local.dev",
        hashed_password=hash_password("triager123"),
        display_name="Triager",
    )
    session.add(user)
    session.add(Project(name="Demo", key="DESK"))
    session.commit()

    def _get_db():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_db
    yield session
    app.dependency_overrides.clear()
    session.close()


@pytest.fixture()
def client(db_session):
    return TestClient(app)


@pytest.fixture()
def auth_header(db_session):
    user = db_session.query(User).first()
    token = make_token(user.id, user.email)
    return {"Authorization": f"Bearer {token}"}
