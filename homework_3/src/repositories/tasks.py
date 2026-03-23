from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from core.database import get_db
from models import Tasks
from schemas import TaskAddingSchema, TaskUpdatingSchema


class TasksRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create(self, task: TaskAddingSchema, author_id: int) -> Tasks:
        task_data = task.model_dump()
        task_data["author_id"] = author_id
        task_db = Tasks(**task_data)
        self.db.add(task_db)
        self.db.commit()
        self.db.refresh(task_db)

        return task_db

    def get_all(self, limit, offset) -> List[Tasks]:
        return self.db.query(Tasks).limit(limit).offset(offset).all()

    def get_by_id(self, task_id: int) -> Optional[Tasks]:
        return self.db.query(Tasks).filter(Tasks.id == task_id).first()

    def update(self, task_id: int, task: TaskUpdatingSchema) -> Optional[Tasks]:
        task_db = self.get_by_id(task_id)

        if not task_db:
            return None

        task_to_update = task.model_dump(exclude_unset=True)

        for field, value in task_to_update.items():
            setattr(task_db, field, value)

        self.db.commit()
        self.db.refresh(task_db)

        return task_db

    def delete(self, task_id: int) -> bool:
        task = self.get_by_id(task_id)

        if task:
            self.db.delete(task)
            self.db.commit()

            return True

        return False
