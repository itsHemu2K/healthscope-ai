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

## Quality checks

```bash
ruff check .
ruff format --check .
mypy src
pytest
```
