from fastapi import APIRouter

from api.comments import router as comments_router
from api.tasks import router as tasks_router
from api.auth import router as auth_router
from api.system import router as system_router


common_router = APIRouter()

common_router.include_router(tasks_router, prefix="/v1")
common_router.include_router(comments_router, prefix="/v1")
common_router.include_router(auth_router, prefix="/v1")
common_router.include_router(system_router)
