from db import init_db, SessionLocal
from fetch_github import fetch_user_profile, fetch_repos, fetch_recent_events, fetch_repo_languages
from store import store_user, store_repos, store_repo_languages, store_events

def run():
    print("initializing db..")
    init_db()

    with SessionLocal() as session:
        print("fetching profile..")
        profile = fetch_user_profile()
        store_user(session, profile)
        print(f"  stored user:  {profile['login']}")

        print("fetching repos..")
        repos = fetch_repos()
        store_repos(session, repos)
        print(f"  stored  {len(repos)} repos")

        print("fetching languages..")
        for repo in repos:
            try:
                langs = fetch_repo_languages(repo["owner"]["login"], repo["name"])
            except Exception as e:
                print(f"  skipping  {repo['name']}:  {e}")
                continue
            store_repo_languages(session, repo["id"], langs)
        print(f"  stored languages for {len(repos)} repos")

        print("fetching events..")
        events = fetch_recent_events(profile["login"])
        store_events(session, events)
        print(f"  stored {len(events)} events")
        session.commit()

    print("done")

if __name__ == "__main__":
    run()