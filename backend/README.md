# HealthScope API

The FastAPI service that powers HealthScope AI.

## Local development

```bash
python -m venv .venv
python -m pip install -e ".[dev]"
alembic upgrade head
uvicorn healthscope.main:app --reload
```

The API is available at `http://localhost:8000`, with OpenAPI documentation at
`/docs` and a health probe at `/api/v1/health`.

## Live data endpoints

`GET /api/v1/hospitals` returns a validated, paginated view of the current CMS
[Hospital General Information](https://data.cms.gov/provider-data/dataset/xubh-q36u)
dataset. Use `limit` (1–100, default 25) and `offset` (default 0) to page through
results. Every response includes the CMS source URL and retrieval timestamp.

The integration has a 10-second upstream timeout by default. Its base URL,
dataset identifier, and timeout can be changed with the variables documented in
`.env.example`.

## Database and migrations

PostgreSQL stores daily CMS hospital snapshots. The snapshot key combines the
CMS dataset ID, UTC retrieval date, and facility ID, so rerunning a refresh on
the same day updates the observation without creating duplicates. A refresh on
a later day preserves a new historical observation.

Set `HEALTHSCOPE_DATABASE_URL` for the target PostgreSQL instance and apply
migrations before starting the API:

```bash
alembic upgrade head
```

Docker Compose supplies the container database URL and applies pending
migrations automatically when the API container starts.

## Quality checks

```bash
ruff check .
ruff format --check .
mypy src
pytest
```
