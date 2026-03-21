from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request

from schemas import BaseTask, TaskAddingSchema, TaskUpdatingSchema
from service import TasksService
from core.security import decode_access_token


router = APIRouter(prefix= "/tasks", tags=["tasks"])


def get_current_username(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не удалось проверить учетные данные")

    token_details = decode_access_token(token)
    if not token_details or not token_details.get("sub"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не удалось проверить учетные данные")

    return token_details["sub"]


@router.post("/")
def add_task(
        payload: TaskAddingSchema,
        request: Request,
        service: TasksService = Depends()
) -> JSONResponse:
    username = get_current_username(request)
    add_result = service.add_task(payload, author_username=username)

    return JSONResponse({
        "message": "Задача добавлена",
        "task": jsonable_encoder(add_result)
    }, status_code=status.HTTP_201_CREATED)


@router.get("/{task_id}")
def get_task(
        task_id: int,
        request: Request,
        service: TasksService = Depends()
) -> JSONResponse:
    username = get_current_username(request)
    author = service.get_user_by_username(username)
    get_result = service.get_task_by_id(task_id)
    if get_result and get_result.author_id == author.id:
        return JSONResponse(jsonable_encoder(get_result), status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Запрещено")


@router.get("/")
def get_tasks_list(
    limit,
    offset,
    request: Request,
    service: TasksService = Depends()
) -> list[BaseTask]:
    username = get_current_username(request)
    get_result = service.get_tasks(limit, offset, author_username=username)
    return get_result


@router.patch("/{book_id}")
def update_task(
        task_id: int,
        payload: TaskUpdatingSchema,
        request: Request,
        service: TasksService = Depends()
):
    username = get_current_username(request)
    author = service.get_user_by_username(username)
    task = service.get_task_by_id(task_id)
    if task.author_id != author.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Запрещено")

    update_result = service.update_task(task_id, payload)
    if update_result:
        return JSONResponse(jsonable_encoder(update_result), status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

@router.delete("/{task_id}")
def delete_task(
        task_id: int,
        request: Request,
        service: TasksService = Depends()
) -> JSONResponse:
    username = get_current_username(request)
    author = service.get_user_by_username(username)
    task = service.get_task_by_id(task_id)
    if task.author_id != author.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Запрещено")

    delete_result = service.delete_task(task_id)
    if delete_result:
        return JSONResponse({
            "status": "Задача удалена"
        }, status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")
