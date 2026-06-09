from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base

class User(Base):
    __tablename__ = "users"

    #github id as PK as it is stable and globally unique for idempotency
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str]
    name: Mapped[str | None]
    public_repos: Mapped[int | None]
    created_at: Mapped[datetime | None] #github account creation
    fetched_at: Mapped[datetime] # when pipeline snapshotted row

    repositories: Mapped[list["Repository"]] = relationship(back_populates="owner")
 
class Repository(Base):
    __tablename__ = "repositories"

    #githubs repo id is stable even if renamed which is why its PK
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str]
    full_name: Mapped[str | None]
    description: Mapped[str |None]
    primary_language: Mapped[str | None]
    stargazers_count: Mapped[int | None]
    forks_count: Mapped[int | None]
    pushed_at: Mapped[datetime | None]
    fetched_at: Mapped[datetime]

    owner: Mapped["User"] = relationship(back_populates="repositories")
    languages: Mapped[list["RepositoryLanguage"]] = relationship(back_populates="repository")

class RepositoryLanguage(Base):
    __tablename__ = "repository_languages"

    #refetching same repos languages updates byte count in place rather than inserting duplicates
    repository_id: Mapped[int] = mapped_column(ForeignKey("repositories.id"), primary_key=True)
    language: Mapped[str] = mapped_column(primary_key=True)
    bytes: Mapped[int]

    repository: Mapped["Repository"] = relationship(back_populates="languages")

class Event(Base):
    __tablename__ = "events"

    #github ids are strings, so column is string
    id: Mapped[str] = mapped_column(primary_key=True)
    type: Mapped[str | None]

    repo_id: Mapped[int | None]
    repo_name: Mapped[str | None]
    created_at: Mapped[datetime | None]
    fetched_at: Mapped[datetime]
