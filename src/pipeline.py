from db import init_db
from fetch_github import fetch_user_profile, fetch_repos, fetch_recent_events, fetch_repo_languages
from store import store_user, store_repos, store_repo_languages, store_events

def run():
    print("initializing db..")
    init_db()

    print("fetching profile..")
    profile = fetch_user_profile()
    store_user(profile)
    print(f"  stored user:  {profile['login']}")

    print("fetching repos..")
    repos = fetch_repos()
    store_repos(repos)
    print(f"  stored  {len(repos)} repos")

    print("fetching languages..")
    for repo in repos:
        try:
            langs = fetch_repo_languages(profile["login"], repo["name"])
            store_repo_languages(repo["id"], langs)
        except Exception as e:
            print(f"  skipping  {repo['name']}:  {e}")
    print(f"  stored languages for {len(repos)} repos")

    print("fetching events..")
    events = fetch_recent_events(profile["login"])
    store_events(events)
    print(f"  stored {len(events)} events")

    print("done")

if __name__ == "__main__":
    run()