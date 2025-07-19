from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.endpoints import (
    health,
    scammer,
    researcher,
    pwner,
    social,
    report,
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    docs_url=f"{settings.API_V1_STR}/docs",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.include_router(
    health.router,
    prefix=f"{settings.API_V1_STR}/health",
)
app.include_router(
    scammer.router,
    prefix=f"{settings.API_V1_STR}/scammer",
)
app.include_router(
    researcher.router,
    prefix=f"{settings.API_V1_STR}/researcher",
)
app.include_router(
    pwner.router,
    prefix=f"{settings.API_V1_STR}/pwner",
)
app.include_router(
    social.router,
    prefix=f"{settings.API_V1_STR}/social",
)
app.include_router(
    report.router,
    prefix=f"{settings.API_V1_STR}/report",
)
