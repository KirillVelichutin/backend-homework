from fastapi import Depends

from repositories import TasksRepository, UsersRepository
from schemas import BaseTask, TaskAddingSchema, TaskUpdatingSchema
from core.exceptions import TaskNotFoundException, UserNotFoundException

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
    
    def add_task(self, new_task: TaskAddingSchema):
        self.check_responsible_user_exists(new_task.responsible_id)
        task_db = self.repo.create(new_task)

        return task_db
    
    def get_task_by_id(self, id: int):
        task_db = self.repo.get_by_id(id)
        
        if not task_db:
            raise TaskNotFoundException(task_id=id)
        
        return task_db
    
    def get_tasks(self, limit, offset) -> list[BaseTask]:
        return self.repo.get_all(limit, offset)
    
    def update_task(self, id: int, payload: TaskUpdatingSchema) -> BaseTask | None:
        db_task = self.repo.update(id, payload)
        
        if not db_task:
            raise TaskNotFoundException(task_id=id)
        
        return db_task
    
    def delete_task(self, id: int) -> bool:
        result = self.repo.delete(id)
        
        if not result:
            raise TaskNotFoundException(task_id=id)
        
        return result
