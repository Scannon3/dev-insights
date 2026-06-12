from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
# fix for pathing
DB_PATH = Path(__file__).resolve().parent.parent / "dev_insights.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"


#false for quiet runs, true to show output ORM generates
engine = create_engine(DATABASE_URL, echo=False)

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
    print(f"database ready at {DB_PATH}")
