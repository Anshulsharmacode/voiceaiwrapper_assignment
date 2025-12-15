# Voice AI Wrapper

Full‑stack app with a Django backend (GraphQL + REST) and a React/Vite frontend. This README covers local setup, Docker build, and how the pieces fit together.

## Requirements
- Python 3.12+
- Node 18+ (or Node 22-alpine via Docker)
- PostgreSQL (used via env vars; SQLite is present for quick local dev)
- `libpq` available when installing `psycopg2-binary` (Dockerfile installs it)

## Backend (Django)
1) Configure env (`Backend/.env`):
```
SECRET_KEY=change-me
DB_NAME=yourdb
DB_USER=youruser
DB_PASSWORD=yourpass
DB_HOST=localhost
DB_PORT=5432
DEBUG=True
```
2) Install deps (uv, preferred):
```
cd Backend
pip install uv
uv sync --frozen --no-dev
```
3) Apply DB migrations:
```
cd Backend
source .venv/bin/activate
python manage.py migrate
```
4) Run the API (includes GraphQL at `/graphql`):
```
python manage.py runserver 0.0.0.0:8000
```
Notes:
- Static files live in `frontend/dist`; `collectstatic` gathers them into `Backend/staticfiles` for production.
- Django templates are pointed at `frontend/dist` so built assets render correctly.

## Frontend (Vite + React)
```
cd frontend
npm install
npm run dev   # http://localhost:5173
npm run build # outputs to frontend/dist
```
Notes:
- Vite base path is `/static/` so Django can serve built assets.
- GraphQL requests expect the Django server (default `http://localhost:8000/graphql`).

## Running with Docker (full stack)
The root `dockerfile` is multi-stage: builds the frontend, installs backend deps with uv, collects static, and runs Django.
```
docker build -t voiceai .
docker run --env-file Backend/.env -p 8000:8000 voiceai
```
Runtime env vars read by Django (set in `.env` or container env):
- `SECRET_KEY`, `DEBUG`
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

## Project structure
- `Backend/` — Django project (`config/` settings, apps: organization, project, task, taskComment)
- `frontend/` — React/Vite UI (GraphQL client)
- `dockerfile` — multi-stage image for production-ish runs

## Useful commands
- Lint frontend: `cd frontend && npm run lint`
- Collect static (prod): `cd Backend && source .venv/bin/activate && python manage.py collectstatic --noinput`
- Reset DB (dev only): delete `Backend/db.sqlite3` then `python manage.py migrate`