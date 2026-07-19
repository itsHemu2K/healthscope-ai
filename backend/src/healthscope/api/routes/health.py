"""Service health endpoints."""

from fastapi import APIRouter, status

from healthscope import __version__
from healthscope.api.dependencies import SettingsDependency
from healthscope.schemas.health import HealthResponse

router = APIRouter(tags=["system"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Check API liveness",
)
def health_check(settings: SettingsDependency) -> HealthResponse:
    """Return process metadata when the API is accepting requests."""

    return HealthResponse(
        service=settings.app_name,
        version=__version__,
        environment=settings.environment,
    )
