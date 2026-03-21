from fastapi import APIRouter

from api.tasks import router as tasks_router
from api.auth import router as auth_router


common_router = APIRouter()

common_router.include_router(tasks_router)
common_router.include_router(auth_router)