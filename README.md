# dev-insights

dev-insights is a service that consolidates your GitHub activity into a view of your coding patterns.

The service is live on Render. The /health endpoint is public.

Example-
curl https://dev-insights-b515.onrender.com/health
json
{"status": "ok"}

What it does

dev-insights authenticates to the GitHub API, pulls your profile, repositories, recent events, and per-repo language breakdowns, and stores them in a relational database. It then exposes that data through a secured API: ranked language statistics by bytes written, a feed of recent events filterable by type, and repository details sorted by most recent activity.

Tech stack
Language: Python 3.12
API framework: FastAPI + Uvicorn
Database: PostgreSQL (production) / SQLite (local), via SQLAlchemy ORM
Data validation: Pydantic + pydantic-settings
HTTP client: requests
Testing: pytest + httpx
Containerization: Docker
CI: GitHub Actions
Hosting: Render (web service + managed Postgres)


dev-insights runs in two stages. An ingestion pipeline (pipeline.py) authenticates to GitHub via OAuth, fetches profile, repo, event, and language data, and writes it to the database in a single atomic transaction with upserts so re-runs update existing records instead of duplicating them. A FastAPI service (app.py) then serves that stored data through read-only endpoints, with a public /health endpoint that verifies database connectivity.


Running it locally

1. Clone and install

git clone https://github.com/Scannon3/dev-insights.git
cd dev-insights
python -m venv .venv
source .venv/Scripts/activate   # Windows Git Bash; use .venv/bin/activate on macOS/Linux
pip install -r requirements.txt

2. Set up env by creating a .env in the repo root:

GITHUB_CLIENT_ID=your_client_id
GITHUB_CLIENT_SECRET=your_client_secret
GITHUB_REDIRECT_URI=your_redirect_uri
API_KEY=your_chosen_api_key

DATABASE_URL is optional and will default to a local SQlite file

3. Authenticate to GitHub (from inside src/):

cd src
python auth.py

This opens a browser for the OAuth flow and writes your access token back to .env.

4. Run the pipeline to fetch and store data:

python pipeline.py

5. Start the API:

uvicorn app:app --reload

The service runs at http://127.0.0.1:8000, with interactive docs at /docs.


All endpoints except /health require an X-Api-Key header.

Health check (public):

curl https://dev-insights-b515.onrender.com/health
json
{"status": "ok"}

Languages gives total bytes per language, ranked:

curl -H "X-Api-Key: YOUR_API_KEY" https://dev-insights-b515.onrender.com/languages
json
[
  {"language": "Python", "bytes": 48210},
  {"language": "JavaScript", "bytes": 12050}
]

Events show recent activity, optionally filtered by type:

curl -H "X-Api-Key: YOUR_API_KEY" https://dev-insights-b515.onrender.com/events
curl -H "X-Api-Key: YOUR_API_KEY" "https://dev-insights-b515.onrender.com/events?type=PushEvent"
json
[
  {
    "id": "48291736",
    "type": "PushEvent",
    "repo_name": "Scannon3/dev-insights",
    "created_at": "2026-08-10T14:32:00"
  }
]

Repositories show repo details, sorted by most recent push:

curl -H "X-Api-Key: YOUR_API_KEY" https://dev-insights-b515.onrender.com/repos
json
[
  {
    "full_name": "Scannon3/dev-insights",
    "description": "GitHub developer activity insights service",
    "primary_language": "Python",
    "pushed_at": "2026-08-10T14:32:00"
  }
]
What this demonstrates

Building dev-insights exercised the full lifecycle of a production backend service:

-External API integration (using githubs Oauth to collect data)
 
-Data modeling and pipelines(fetch, store, serve)

-A secured REST API(FastAPI endpoints gated behind api key authentication)

-Testing(pytest for endpoint behavior/on conflict handling)

-Containerization and CI/CD(Dockerfile, Github Actions, auto deployment on Render)

-Deployment and observability(live service with a health check endpoint to verify connectivity)