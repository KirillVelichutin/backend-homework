from fastapi import Depends, HTTPException, status

from repositories import TasksRepository, UsersRepository
from service.storage import StorageService
from schemas import BaseTask, TaskAddingSchema, TaskUpdatingSchema
from core.exceptions import TaskNotFound, UserNotFoundException


class TasksService:
    def __init__(
        self,
        repository: TasksRepository = Depends(),
        users_repository: UsersRepository = Depends(),
        storage_service: StorageService = Depends(),
    ):
        self.repo = repository
        self.users_repo = users_repository
        self.storage = storage_service

    async def check_responsible_user_exists(self, user_id: int):
        if not await self.users_repo.get_by_id(user_id):
            raise UserNotFoundException(user_id=user_id)

    async def get_user_by_username(self, username: str):
        db_user = await self.users_repo.get_by_username(username)
        if not db_user:
            raise UserNotFoundException(user_id=-1)

        return db_user

    async def create_task(self, new_task: TaskAddingSchema, author_username: str):
        await self.check_responsible_user_exists(new_task.responsible_id)
        author = await self.get_user_by_username(author_username)
        task_db = await self.repo.create(new_task, author_id=author.id)

        return task_db

    async def get_task_by_id(self, id: int):
        task_db = await self.repo.get_by_id(id)

        if not task_db:
            raise TaskNotFound(task_id=id)

        return task_db

    async def get_tasks(self, limit, offset) -> list[BaseTask]:
        return await self.repo.get_all(limit, offset)

    async def update_task(self, id: int, payload: TaskUpdatingSchema) -> BaseTask | None:
        db_task = await self.repo.update(id, payload)

        if not db_task:
            raise TaskNotFound(task_id=id)

        return db_task

    async def delete_task(self, id: int) -> bool:
        result = await self.repo.delete(id)

        if not result:
            raise TaskNotFound(task_id=id)

        return result

    async def upload_avatar(self, task_id: int, username: str, file) -> str:
        author = await self.get_user_by_username(username)
        task = await self.get_task_by_id(task_id)
        if task.author_id != author.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Запрещено")

        return await self.storage.upload_task_avatar(task_id, file)
