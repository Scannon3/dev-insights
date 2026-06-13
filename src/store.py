from datetime import datetime, timezone
from sqlalchemy.dialects.sqlite import insert
from db import SessionLocal
from models import User, Repository, RepositoryLanguage, Event


def store_user(profile: dict) -> None:
    with SessionLocal() as session:
        stmt = insert(User).values(
            id=profile["id"],
            login=profile["login"],
            name=profile.get("name"),
            public_repos=profile.get("public_repos"),
            created_at=datetime.fromisoformat(profile["created_at"]),
            fetched_at=datetime.now(timezone.utc),
        ).on_conflict_do_update(
            index_elements=["id"],
            set_=dict(
                login=profile["login"],
                name=profile.get("name"),
                public_repos=profile.get("public_repos"),
                fetched_at=datetime.now(timezone.utc)
            )
        )
        session.execute(stmt)
        session.commit()

def store_repos(repos: list[dict]) -> None:
    with SessionLocal() as session:
        for repo in repos:
            stmt = insert(Repository).values(
                id=repo["id"],
                user_id = repo["owner"]["id"],
                name = repo["name"],
                full_name = repo.get("full_name"),
                description=repo.get("description"),
                primary_language=repo.get("language"),
                stargazers_count=repo.get("stargazers_count"),
                forks_count=repo.get("forks_count"),
                pushed_at=datetime.fromisoformat(repo["pushed_at"]) if repo.get("pushed_at") else None,
                fetched_at=datetime.now(timezone.utc),
            ).on_conflict_do_update(
                index_elements=["id"],
                set_=dict(
                    name=repo["name"],
                    full_name=repo.get("full_name"),
                    description=repo.get("description"),
                    primary_language=repo.get("language"),
                    stargazers_count=repo.get("stargazers_count"),
                    forks_count=repo.get("forks_count"),
                    pushed_at=datetime.fromisoformat(repo["pushed_at"]) if repo.get("pushed_at") else None,
                    fetched_at=datetime.now(timezone.utc),
                    )
            )
            session.execute(stmt)
        session.commit()

def store_repo_languages(repository_id: int, langs: dict[str,int]) -> None:
    with SessionLocal() as session:
        for language, bytes_count in langs.items():
            stmt = insert(RepositoryLanguage).values(
                repository_id=repository_id,
                language=language,
                bytes=bytes_count,
            ).on_conflict_do_update(
                index_elements=["repository_id", "language"],
                set_=dict(bytes=bytes_count)
            )
            session.execute(stmt)
        session.commit()

def store_events(events: list[dict]) -> None:
    with SessionLocal() as session:
        for event in events:
            stmt = insert(Event).values(
                id=event["id"],
                type=event.get("type"),
                repo_id=event.get("repo", {}).get("id"),
                repo_name=event.get("repo", {}).get("name"),
                created_at=datetime.fromisoformat(event["created_at"]) if event.get("created_at") else None,
                fetched_at=datetime.now(timezone.utc),
            ).on_conflict_do_nothing(index_elements=["id"])
            session.execute(stmt)
        session.commit()