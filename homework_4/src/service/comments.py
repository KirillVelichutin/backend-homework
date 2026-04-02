from fastapi import Depends, HTTPException, status

from repositories import CommentsRepository, TasksRepository, UsersRepository
from schemas import BaseComment, CommentAddingSchema
from core.exceptions import CommentNotFound, TaskNotFound, UserNotFoundException


class CommentsService:
    def __init__(
        self,
        repository: CommentsRepository = Depends(),
        tasks_repository: TasksRepository = Depends(),
        users_repository: UsersRepository = Depends(),
    ):
        self.repo = repository
        self.tasks_repo = tasks_repository
        self.users_repo = users_repository

    async def get_user_by_username(self, username: str):
        db_user = await self.users_repo.get_by_username(username)
        if not db_user:
            raise UserNotFoundException(user_id=-1)

        return db_user

    async def get_task_by_id(self, task_id: int):
        task_db = await self.tasks_repo.get_by_id(task_id)
        if not task_db:
            raise TaskNotFound(task_id=task_id)

        return task_db

    async def get_comment_by_id(self, task_id: int, comment_id: int):
        comment = await self.repo.get_by_id(comment_id)
        if not comment or comment.task_id != task_id:
            raise CommentNotFound(comment_id=comment_id)

        return comment

    async def add_comment(self, task_id: int, payload: CommentAddingSchema, username: str) -> BaseComment:
        user = await self.get_user_by_username(username)
        await self.get_task_by_id(task_id)
        return await self.repo.create(task_id, user.id, payload)

    async def get_comments(self, task_id: int, username: str) -> list[BaseComment]:
        await self.get_user_by_username(username)
        await self.get_task_by_id(task_id)
        return await self.repo.get_by_task_id(task_id)

    async def delete_comment(self, task_id: int, comment_id: int, username: str) -> None:
        user = await self.get_user_by_username(username)
        await self.get_task_by_id(task_id)
        comment = await self.get_comment_by_id(task_id, comment_id)
        if comment.author_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Запрещено")
        await self.repo.delete(comment)
