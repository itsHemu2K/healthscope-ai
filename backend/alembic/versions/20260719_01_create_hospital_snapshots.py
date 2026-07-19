"""Create daily CMS hospital snapshots.

Revision ID: 20260719_01
Revises:
Create Date: 2026-07-19
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260719_01"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the table that preserves daily CMS hospital observations."""

    op.create_table(
        "hospital_snapshots",
        sa.Column("source_dataset_id", sa.String(length=32), nullable=False),
        sa.Column("snapshot_date", sa.Date(), nullable=False),
        sa.Column("facility_id", sa.String(length=16), nullable=False),
        sa.Column("retrieved_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("facility_name", sa.String(length=255), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.Column("city", sa.String(length=128), nullable=False),
        sa.Column("state", sa.String(length=2), nullable=False),
        sa.Column("zip_code", sa.String(length=10), nullable=False),
        sa.Column("county", sa.String(length=128), nullable=False),
        sa.Column("telephone", sa.String(length=32), nullable=False),
        sa.Column("hospital_type", sa.String(length=128), nullable=False),
        sa.Column("ownership", sa.String(length=128), nullable=False),
        sa.Column("emergency_services", sa.Boolean(), nullable=False),
        sa.Column("birthing_friendly", sa.Boolean(), nullable=True),
        sa.Column("overall_rating", sa.Integer(), nullable=True),
        sa.CheckConstraint(
            "overall_rating BETWEEN 1 AND 5",
            name=op.f("ck_hospital_snapshots_overall_rating_range"),
        ),
        sa.CheckConstraint(
            "length(state) = 2",
            name=op.f("ck_hospital_snapshots_state_length"),
        ),
        sa.PrimaryKeyConstraint(
            "source_dataset_id",
            "snapshot_date",
            "facility_id",
            name="pk_hospital_snapshots",
        ),
    )
    op.create_index(
        "ix_hospital_snapshots_snapshot_date_state",
        "hospital_snapshots",
        ["snapshot_date", "state"],
        unique=False,
    )


def downgrade() -> None:
    """Drop CMS hospital snapshots."""

    op.drop_index(
        "ix_hospital_snapshots_snapshot_date_state",
        table_name="hospital_snapshots",
    )
    op.drop_table("hospital_snapshots")
