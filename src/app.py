from fastapi import FastAPI, Depends
from db import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from schemas import LanguageStat, EventOut, RepoOut
from models import RepositoryLanguage

app = FastAPI()

def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.get("/languages", response_model=list[LanguageStat])
def get_languages(session: Session = Depends(get_db)):
    stmt= select(RepositoryLanguage.language,
                  func.sum(RepositoryLanguage.bytes).label("bytes")).group_by(RepositoryLanguage.language).order_by(func.sum(RepositoryLanguage.bytes).desc()
                )
    rows = session.execute(stmt).all()
    return [LanguageStat(language=row.language, bytes=row.bytes) for row in rows]