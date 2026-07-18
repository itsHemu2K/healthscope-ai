# HealthScope AI

HealthScope AI is a production-oriented healthcare intelligence platform for
ingesting live public datasets, preserving historical snapshots, calculating
healthcare KPIs, and exposing insights through APIs and interactive dashboards.

## Project goals

- Ingest reproducible data from public sources such as CMS, CDC, Census, and FDA.
- Build validated, observable ETL pipelines with retries and incremental loading.
- Store analytics-ready healthcare data in PostgreSQL.
- Provide typed FastAPI endpoints and a responsive React dashboard.
- Run locally with Docker and ship through tested CI/CD workflows.

## Planned stack

- Python, FastAPI, SQLAlchemy, Pandas, and Pydantic
- PostgreSQL
- React, TypeScript, Vite, Tailwind CSS, and Recharts
- Docker Compose and GitHub Actions

## Status

Initial project setup is in progress. The first milestone targets a complete local
development environment, three live healthcare data sources, REST APIs, dashboard
visualizations, automated tests, and architecture documentation.

## Data policy

Only live, publicly available healthcare datasets are used. No fabricated CSV
datasets or patient-level protected health information belong in this repository.

