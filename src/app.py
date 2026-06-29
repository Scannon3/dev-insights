from fastapi import FastAPI, Depends, Header, HTTPException
from db import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from schemas import LanguageStat, EventOut, RepoOut
from models import RepositoryLanguage, Event, Repository
from config import settings

app = FastAPI()

def require_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid Api Key") 
    
def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.get("/languages", response_model=list[LanguageStat])
def get_languages(session: Session = Depends(get_db), _ = Depends(require_api_key)):
    stmt= select(RepositoryLanguage.language,
                  func.sum(RepositoryLanguage.bytes).label("bytes")).group_by(RepositoryLanguage.language).order_by(func.sum(RepositoryLanguage.bytes).desc()
                )
    rows = session.execute(stmt).all()
    return [LanguageStat(language=row.language, bytes=row.bytes) for row in rows]

@app.get("/events", response_model=list[EventOut])
def get_events(type: str | None = None, session: Session = Depends(get_db), _ = Depends(require_api_key)):
    stmt = select(Event.id, Event.type, Event.repo_name, Event.created_at).order_by(Event.created_at.desc())
    if type is not None:
        stmt = stmt.where(Event.type == type)
    rows = session.execute(stmt).all()
    return [EventOut(id=row.id, type=row.type, repo_name=row.repo_name, created_at = row.created_at) for row in rows]

@app.get("/repos", response_model=list[RepoOut])
def get_repos(session: Session = Depends(get_db), _ = Depends(require_api_key)):
    stmt = select(Repository.full_name, Repository.description, Repository.primary_language, Repository.pushed_at).order_by(Repository.pushed_at.desc())
    rows = session.execute(stmt).all()
    return [RepoOut(full_name=row.full_name, description=row.description, primary_language=row.primary_language, pushed_at=row.pushed_at) for row in rows]