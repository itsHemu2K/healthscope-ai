"""Hospital intelligence endpoints backed by live CMS data."""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from healthscope.clients.cms import (
    CMSClientDependency,
    CMSClientError,
    CMSUpstreamTimeoutError,
)
from healthscope.schemas.hospitals import HospitalPage

router = APIRouter(prefix="/hospitals", tags=["hospitals"])
PageLimit = Annotated[int, Query(ge=1, le=100)]
PageOffset = Annotated[int, Query(ge=0)]


@router.get(
    "",
    response_model=HospitalPage,
    status_code=status.HTTP_200_OK,
    summary="List current Medicare-registered hospitals",
)
async def list_hospitals(
    cms_client: CMSClientDependency,
    limit: PageLimit = 25,
    offset: PageOffset = 0,
) -> HospitalPage:
    """Return a validated page from CMS Hospital General Information."""

    try:
        return await cms_client.fetch_hospitals(limit=limit, offset=offset)
    except CMSUpstreamTimeoutError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="CMS Provider Data did not respond before the request deadline.",
        ) from exc
    except CMSClientError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="CMS Provider Data is temporarily unavailable.",
        ) from exc
