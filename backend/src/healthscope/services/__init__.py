"""Application services for healthcare data workflows."""

from healthscope.services.ingestion import (
    HospitalIngestionError,
    HospitalIngestionResult,
    ingest_hospital_snapshots,
)

__all__ = [
    "HospitalIngestionError",
    "HospitalIngestionResult",
    "ingest_hospital_snapshots",
]
