from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from db import Base
from models import Event
from store import store_events

event_v1 = {"id": "123", "type": "PushEvent"}
event_v2 = {"id": "123", "type": "WatchEvent"}

test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False
)

TestSessionLocal = sessionmaker(bind=test_engine)

def init_test_db() -> None:
    Base.metadata.create_all(test_engine)

def test_store_events():
    init_test_db()
    session = TestSessionLocal()
    
    store_events(session, [event_v1])
    store_events(session, [event_v2])
    session.commit()
    event = session.query(Event).first()
    assert event.type == "PushEvent"