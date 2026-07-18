"""FastAPI application factory and ASGI entry point."""

from fastapi import FastAPI

from healthscope import __version__
from healthscope.api.routes.health import router as health_router
from healthscope.config import Settings, get_settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build an application instance with explicit, testable settings."""

    resolved_settings = settings or get_settings()
    application = FastAPI(
        title=resolved_settings.app_name,
        version=__version__,
        debug=resolved_settings.debug,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
    if settings is not None:

        def provide_settings() -> Settings:
            return resolved_settings

        application.dependency_overrides[get_settings] = provide_settings

    application.include_router(health_router, prefix=resolved_settings.api_prefix)
    return application


app = create_app()
