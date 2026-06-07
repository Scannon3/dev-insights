import secrets
from pathlib import Path
import webbrowser
from urllib.parse import urlencode,urlparse,parse_qs

import requests

from config import settings

def build_auth_url(state:str) -> str:
    #build github auth url user wil visit
    params = {
        "client_id": settings.github_client_id,
        "redirect_uri": settings.github_redirect_uri,
        "scope": "read:user repo",
        "state": state,
    }
    return "https://github.com/login/oauth/authorize?" + urlencode(params)

def exchange_code_for_token(code:str) -> str:
    #send auth code to github and get back access token
    response = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": settings.github_client_id,
            "client_secret": settings.github_client_secret,
            "code": code,
            "redirect_uri": settings.github_redirect_uri,


        },
    )
    response.raise_for_status()

    token_data= response.json()
    if "error" in token_data:
        raise ValueError(f"Token exchange failed: {token_data['error_description']}")
    
    return token_data["access_token"]

if __name__ == "__main__":
    #generate random state value and build auth url
    state = secrets.token_urlsafe(16)
    auth_url = build_auth_url(state)

    #open browser so user can auth
    print(f"\nOpening your browser to authorize the app...\n")
    print(f"If it doesn't open, visit this url manually:\n{auth_url}\n")
    webbrowser.open(auth_url)

    #user pastes back the callback url containing codde
    callback_url = input("after authorizing, paste full url from browsers address bar:\n> ")

    #extract and verify code and state from callback url
    params = parse_qs(urlparse(callback_url).query)

    returned_state = params.get("state", [None])[0]
    if returned_state != state:
        raise ValueError("state mismatch - aborting")
    
    code = params.get("code", [None])[0]
    if not code:
        raise ValueError("no auth code found in url")
    
    #exchange code for access token
    print("\nexchanging code for access token...")
    token = exchange_code_for_token(code)
     # save the token to .env so we can reuse it
    env_path = Path(__file__).resolve().parent.parent / ".env"
    with open(env_path, "a") as f:
        f.write(f"\nGITHUB_ACCESS_TOKEN={token}\n")
    print(f"\nsuccess! token saved to .env (starts with {token[:8]}...)")

