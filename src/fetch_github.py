#fetch github data using stored access token

import requests
from config import settings

BASE_URL = "https://api.github.com"

def get_headers() -> dict[str, str]:
    #build auth headers for github api requests
    if settings.github_access_token is None:
        raise RuntimeError("no access token found.. run auth.py first")
    return {
        "Authorization": f"Bearer {settings.github_access_token}",
        "Accept": "application/vnd.github+json",

    }

def fetch_user_profile() -> dict:
    #fetch authenticated user's profile
    response = requests.get(f"{BASE_URL}/user", headers=get_headers())
    response.raise_for_status()
    return response.json()

def fetch_repos() -> list[dict]:
    #fetch authenticated users repos
    response = requests.get(
        f"{BASE_URL}/user/repos",
        headers=get_headers(),
        params={"sort": "updated", "per_page": 30},
    )
    response.raise_for_status()
    return response.json()

def fetch_recent_events(username: str) -> list[dict]:
    #fetch recent public events for the user
    response = requests.get(
        f"{BASE_URL}/users/{username}/events",
        headers=get_headers(),
        params={"per_page": 30},
    )
    response.raise_for_status()
    return response.json()
def fetch_repo_languages(owner: str, repo:str) -> dict[str,list]:
    #fetch byte breakdown of languages in repo
    response = requests.get(
        f"{BASE_URL}/repos/{owner}/{repo}/languages",
        headers=get_headers(),
    )
    response.raise_for_status()
    return response.json()

if __name__=="__main__":
    #profile
    profile = fetch_user_profile()
    print(f"authenticated as: {profile['login']}")
    print(f"Public repos: {profile['public_repos']}\n")

    #repos
    repos = fetch_repos()
    print(f"--- Your {len(repos)} most recently updated repos ---")
    for repo in repos[:10]:
        lang = repo.get("language") or "unknown"
        print(f"  {repo['name']:30s}  {lang:15s} stars:  {repo['stargazers_count']}")
    
    #recent events
    print(f"\n--- recent activity---")
    events = fetch_recent_events(profile["login"])
    for event in events[:10]:
        repo_name = event.get("repo", {}).get("name", "unknown")
        print(f"  {event['type']:25s}  {repo_name}")

    #language breakdwon sample
    if repos:
        sample = repos[0]
        langs = fetch_repo_languages(profile["login"], sample["name"])
        print(f"\n--- languages in '{sample['name']}'---")
        for lang, bytes_count in langs.items():
            print(f"  {lang:20s}  {bytes_count:,} bytes")

