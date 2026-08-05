from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import settings

# Local default: SQLite file at repo root. Cloud: DATABASE_URL from env (Postgres).
DEFAULT_SQLITE = f"sqlite:///{Path(__file__).resolve().parent.parent / 'dev_insights.db'}"
DATABASE_URL = settings.database_url or DEFAULT_SQLITE

#false for quiet runs, true to show output ORM generates
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)

#fresh session for each conversation with db
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    #every model subclasses this
    pass

def init_db() -> None:
    #import here to avoid circular import (models.py)
    import models

    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
    print(f"database ready at {DATABASE_URL}")
