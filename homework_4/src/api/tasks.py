from fastapi import APIRouter, status, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request

from schemas import BaseTask, TaskAddingSchema, TaskUpdatingSchema
from service import TasksService
from core.security import decode_access_token


router = APIRouter(prefix="/tasks", tags=["tasks"])


async def get_current_username(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не удалось проверить учетные данные")

    token_details = await decode_access_token(token)
    if not token_details or not token_details.get("sub"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не удалось проверить учетные данные")

    return token_details["sub"]


@router.post("/")
async def create_task(
        payload: TaskAddingSchema,
        request: Request,
        service: TasksService = Depends()
) -> JSONResponse:
    username = await get_current_username(request)
    add_result = await service.create_task(payload, author_username=username)

    return JSONResponse({
        "message": "Задача добавлена",
        "task": jsonable_encoder(add_result)
    }, status_code=status.HTTP_201_CREATED)


@router.get("/{task_id}")
async def get_task(
        task_id: int,
        request: Request,
        service: TasksService = Depends()
) -> JSONResponse:
    await get_current_username(request)
    get_result = await service.get_task_by_id(task_id)

    return JSONResponse(jsonable_encoder(get_result), status.HTTP_200_OK)


@router.get("/")
async def get_tasks_list(
        request: Request,
        limit: int = 10,
        offset: int = 0,
        service: TasksService = Depends()
) -> list[BaseTask]:
    await get_current_username(request)
    get_result = await service.get_tasks(limit, offset)
    return get_result


@router.patch("/{task_id}")
async def update_task(
        task_id: int,
        payload: TaskUpdatingSchema,
        request: Request,
        service: TasksService = Depends()
):
    username = await get_current_username(request)
    author = await service.get_user_by_username(username)
    task = await service.get_task_by_id(task_id)
    if task.author_id != author.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Запрещено")

    update_result = await service.update_task(task_id, payload)
    return JSONResponse(jsonable_encoder(update_result), status.HTTP_200_OK)


@router.delete("/{task_id}")
async def delete_task(
        task_id: int,
        request: Request,
        service: TasksService = Depends()
) -> JSONResponse:
    username = await get_current_username(request)
    author = await service.get_user_by_username(username)
    task = await service.get_task_by_id(task_id)
    if task.author_id != author.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Запрещено")

    delete_result = await service.delete_task(task_id)
    if delete_result:
        return JSONResponse({
            "status": "Задача удалена"
        }, status.HTTP_200_OK)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")


@router.post("/{task_id}/upload-avatar")
async def upload_task_avatar(
        task_id: int,
        request: Request,
        file: UploadFile = File(...),
        service: TasksService = Depends()
) -> JSONResponse:
    username = await get_current_username(request)
    file_url = await service.upload_avatar(task_id, username, file)

    return JSONResponse(
        {"url": file_url},
        status_code=status.HTTP_201_CREATED,
    )
