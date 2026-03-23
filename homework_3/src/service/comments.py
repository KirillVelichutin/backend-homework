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

    def get_user_by_username(self, username: str):
        db_user = self.users_repo.get_by_username(username)
        if not db_user:
            raise UserNotFoundException(user_id=-1)

        return db_user

    def get_task_by_id(self, task_id: int):
        task_db = self.tasks_repo.get_by_id(task_id)
        if not task_db:
            raise TaskNotFound(task_id=task_id)

        return task_db

    def ensure_task_access(self, task_id: int, username: str):
        user = self.get_user_by_username(username)
        task = self.get_task_by_id(task_id)

        if task.author_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Запрещено")

        return task

    def get_comment_by_id(self, task_id: int, comment_id: int):
        comment = self.repo.get_by_id(comment_id)
        if not comment or comment.task_id != task_id:
            raise CommentNotFound(comment_id=comment_id)

        return comment

    def add_comment(self, task_id: int, payload: CommentAddingSchema, username: str) -> BaseComment:
        self.ensure_task_access(task_id, username)
        return self.repo.create(task_id, payload)

    def get_comments(self, task_id: int, username: str) -> list[BaseComment]:
        self.ensure_task_access(task_id, username)
        return self.repo.get_by_task_id(task_id)

    def delete_comment(self, task_id: int, comment_id: int, username: str) -> None:
        self.ensure_task_access(task_id, username)
        comment = self.get_comment_by_id(task_id, comment_id)
        self.repo.delete(comment)
