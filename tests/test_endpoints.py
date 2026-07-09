from datetime import datetime, timezone
from fastapi.testclient import TestClient
from config import settings
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from models import User, Repository, RepositoryLanguage, Event
from db import Base
from app import app
from app import get_db


test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False
)

TestSessionLocal = sessionmaker(bind=test_engine)

def init_test_db() -> None:
    Base.metadata.create_all(test_engine)

def override_get_db():
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_get_repos():
    init_test_db()

    session = TestSessionLocal()
    session.add(User(id=1, login="octocat", fetched_at=datetime.now(timezone.utc)))
    session.add(Repository(id=1, user_id=1, name="hello-world", full_name="nametest", fetched_at=datetime.now(timezone.utc)))
    session.commit()
    session.close()

    response = client.get("/repos", headers={"X-API-Key": settings.api_key})

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    assert data[0]["full_name"] == "nametest"

