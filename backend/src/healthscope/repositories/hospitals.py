"""Persistence operations for CMS hospital snapshots."""

from datetime import datetime
from typing import cast

from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import insert as postgresql_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.orm import Session
from sqlalchemy.sql.base import Executable

from healthscope.models.hospitals import HospitalSnapshot
from healthscope.schemas.hospitals import Hospital

_KEY_COLUMNS = ("source_dataset_id", "snapshot_date", "facility_id")


def _snapshot_values(snapshot: HospitalSnapshot) -> dict[str, object]:
    """Convert an ORM snapshot into values accepted by a bulk insert."""

    table = HospitalSnapshot.__table__
    return {column.name: getattr(snapshot, column.name) for column in table.columns}


def _upsert_statement(
    table: Table,
    values: list[dict[str, object]],
    dialect_name: str,
) -> Executable:
    """Build a native idempotent upsert for supported database dialects."""

    if dialect_name == "postgresql":
        statement = postgresql_insert(table).values(values)
        update_values = {
            column.name: getattr(statement.excluded, column.name)
            for column in table.columns
            if column.name not in _KEY_COLUMNS
        }
        return statement.on_conflict_do_update(
            index_elements=[table.c[column] for column in _KEY_COLUMNS],
            set_=update_values,
        )
    if dialect_name == "sqlite":
        statement_sqlite = sqlite_insert(table).values(values)
        update_values = {
            column.name: getattr(statement_sqlite.excluded, column.name)
            for column in table.columns
            if column.name not in _KEY_COLUMNS
        }
        return statement_sqlite.on_conflict_do_update(
            index_elements=[table.c[column] for column in _KEY_COLUMNS],
            set_=update_values,
        )
    raise ValueError(f"Unsupported hospital snapshot database dialect: {dialect_name}")


def upsert_hospital_snapshots(
    session: Session,
    hospitals: list[Hospital],
    *,
    source_dataset_id: str,
    retrieved_at: datetime,
) -> int:
    """Insert or refresh one daily snapshot batch and return its record count."""

    snapshots = [
        HospitalSnapshot.from_hospital(
            hospital,
            source_dataset_id=source_dataset_id,
            retrieved_at=retrieved_at,
        )
        for hospital in hospitals
    ]
    facility_ids = [snapshot.facility_id for snapshot in snapshots]
    if len(facility_ids) != len(set(facility_ids)):
        raise ValueError("Hospital snapshot batches must contain unique facility IDs")
    if not snapshots:
        return 0

    table = cast(Table, HospitalSnapshot.__table__)
    statement = _upsert_statement(
        table,
        [_snapshot_values(snapshot) for snapshot in snapshots],
        session.get_bind().dialect.name,
    )
    session.execute(statement)
    return len(snapshots)
