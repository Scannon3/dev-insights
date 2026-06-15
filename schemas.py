from datetime import datetime
from pydantic import BaseModel   

class LanguageStat(BaseModel):
    language: str
    bytes: int

class EventOut(BaseModel):
    id: str
    type: str | None
    repo_name: str | None
    created_at: datetime | None

class RepoOut(BaseModel):
    full_name: str | None
    description: str | None
    primary_language: str | None
    pushed_at: datetime | None
