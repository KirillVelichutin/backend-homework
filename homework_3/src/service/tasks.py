from fastapi import Depends

from repositories import TasksRepository, UsersRepository
from schemas import BaseTask, TaskAddingSchema, TaskUpdatingSchema
from core.exceptions import TaskNotFound, UserNotFoundException


class TasksService:
    def __init__(
        self,
        repository: TasksRepository = Depends(),
        users_repository: UsersRepository = Depends(),
    ):
        self.repo = repository
        self.users_repo = users_repository

    def check_responsible_user_exists(self, user_id: int):
        if not self.users_repo.get_by_id(user_id):
            raise UserNotFoundException(user_id=user_id)

    def get_user_by_username(self, username: str):
        db_user = self.users_repo.get_by_username(username)
        if not db_user:
            raise UserNotFoundException(user_id=-1)

        return db_user

    def add_task(self, new_task: TaskAddingSchema, author_username: str):
        self.check_responsible_user_exists(new_task.responsible_id)
        author = self.get_user_by_username(author_username)
        task_db = self.repo.create(new_task, author_id=author.id)

        return task_db

    def get_task_by_id(self, id: int):
        task_db = self.repo.get_by_id(id)

        if not task_db:
            raise TaskNotFound(task_id=id)

        return task_db

    def get_tasks(self, limit, offset, author_username: str) -> list[BaseTask]:
        author = self.get_user_by_username(author_username)
        return self.repo.get_all(limit, offset, author.id)

    def update_task(self, id: int, payload: TaskUpdatingSchema) -> BaseTask | None:
        db_task = self.repo.update(id, payload)

        if not db_task:
            raise TaskNotFound(task_id=id)

        return db_task

    def delete_task(self, id: int) -> bool:
        result = self.repo.delete(id)

        if not result:
            raise TaskNotFound(task_id=id)

        return result
