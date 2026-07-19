# HealthScope API

The FastAPI service that powers HealthScope AI.

## Local development

```bash
python -m venv .venv
python -m pip install -e ".[dev]"
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

## Quality checks

```bash
ruff check .
ruff format --check .
mypy src
pytest
```
