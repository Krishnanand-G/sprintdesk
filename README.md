# SprintDesk

Agile workspace for small teams: projects, sprints, and tickets with a simple board view.

## Stack

FastAPI, SQLAlchemy, React (Vite), Postgres in Docker, SQLite for local dev.

## Run backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Run frontend

```bash
cd frontend
npm install
npm run dev
```

Seed login: `triager@local.dev` / `triager123`

Copy `.env.example` to `.env` when using Postgres. Without `DATABASE_URL` the API uses `sprintdesk.db`.

## Tests

```bash
cd backend && pytest -q
cd ../frontend && npm test
```
