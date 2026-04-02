import asyncio

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.database import get_db
from core.minio import get_minio_client


router = APIRouter(tags=["system"])


@router.get("/health")
async def healthcheck(
    db: AsyncSession = Depends(get_db),
    minio_client=Depends(get_minio_client),
) -> JSONResponse:
    db_status = "ok"
    minio_status = "ok"

    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        db_status = "error"

    try:
        await asyncio.to_thread(minio_client.list_buckets)
    except Exception:
        minio_status = "error"

    overall_status = "ok"
    status_code = status.HTTP_200_OK

    if db_status == "error" or minio_status == "error":
        overall_status = "error"
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return JSONResponse(
        {
            "status": overall_status,
            "database": db_status,
            "minio": minio_status,
        },
        status_code=status_code,
    )


@router.get("/info")
async def app_info() -> JSONResponse:
    return JSONResponse(
        {
            "version": settings.app_version,
            "environment": settings.app_env,
        },
        status_code=status.HTTP_200_OK,
    )
