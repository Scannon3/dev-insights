from datetime import datetime
from pydantic import BaseModel   
from enum import Enum

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

class EventType(str, Enum):
    push = "PushEvent"
    pullreqevent = "PullRequestEvent"
    create = "CreateEvent"
    delete = "DeleteEvent"
    watch = "WatchEvent"
    fork = "ForkEvent"
    issues = "IssuesEvent"
    issuescommon = "IssueCommentEvent"
    review = "PullRequestReviewEvent"
    release = "ReleaseEvent"
    public = "PublicEvent"