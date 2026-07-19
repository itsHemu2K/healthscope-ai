# HealthScope AI architecture

HealthScope AI currently uses a small layered backend so public-data contracts,
application behavior, and storage can evolve independently.

## Backend flow

1. FastAPI routes validate HTTP parameters and map upstream failures to stable
   service responses.
2. Typed source clients retrieve and validate records from official public
   healthcare APIs. The current client uses CMS Provider Data Catalog dataset
   `xubh-q36u`; no bundled or fabricated healthcare dataset is used.
3. Repository functions persist validated records through SQLAlchemy. Daily CMS
   hospital observations use PostgreSQL-native upserts and a composite key of
   source dataset, UTC snapshot date, and facility ID.
4. Alembic owns all database schema changes. Application startup does not call
   `create_all`; deployment or Docker Compose applies versioned migrations.

## Current deployment boundary

Docker Compose runs the FastAPI container and PostgreSQL 17. PostgreSQL data is
kept in a named volume, the API waits for database readiness, and migrations run
before Uvicorn starts. Runtime secrets and production connection details must be
provided through environment variables rather than committed configuration.

## Next boundary

The next increment should add an explicit ingestion service or CLI command that
pages through the live CMS dataset, assigns one retrieval timestamp to the full
run, writes batches through the idempotent repository, and reports counts and
failures. That service can later be scheduled without embedding ETL work in API
startup.
