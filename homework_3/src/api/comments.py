from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from api.tasks import get_current_username
from schemas import BaseComment, CommentAddingSchema
from service import CommentsService


router = APIRouter(prefix="/tasks/{task_id}/comments", tags=["comments"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_comment(
        task_id: int,
        payload: CommentAddingSchema,
        request: Request,
        service: CommentsService = Depends()
) -> JSONResponse:
    username = get_current_username(request)
    comment = service.add_comment(task_id, payload, username)
    return JSONResponse(jsonable_encoder(comment), status_code=status.HTTP_201_CREATED)


@router.get("/")
def get_comments(
        task_id: int,
        request: Request,
        service: CommentsService = Depends()
) -> list[BaseComment]:
    username = get_current_username(request)
    return service.get_comments(task_id, username)


@router.delete("/{comment_id}")
def delete_comment(
        task_id: int,
        comment_id: int,
        request: Request,
        service: CommentsService = Depends()
) -> JSONResponse:
    username = get_current_username(request)
    service.delete_comment(task_id, comment_id, username)
    return JSONResponse({"status": "Комментарий удален"}, status_code=status.HTTP_200_OK)
