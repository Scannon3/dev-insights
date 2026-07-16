from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from db import Base
from models import Repository, User
from store import store_repos

test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False
)

TestSessionLocal = sessionmaker(bind=test_engine)

def init_test_db() -> None:
    Base.metadata.create_all(test_engine)

def test_store_repos():
    init_test_db()
    session = TestSessionLocal()
    repo_dict = {
        "id": 123,
        "name": "repo1",
        "full_name": "Scannon3/repo1",
        "owner": {"id": 1},
    }
    store_repos(session, [repo_dict])
    store_repos(session, [repo_dict])
    session.commit()
    count = session.query(Repository).count()
    assert count == 1

