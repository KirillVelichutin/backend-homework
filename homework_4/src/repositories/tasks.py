from fastapi import Depends
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models import Tasks
from schemas import TaskAddingSchema, TaskUpdatingSchema


class TasksRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create(self, task: TaskAddingSchema, author_id: int) -> Tasks:
        task_data = task.model_dump()
        task_data["author_id"] = author_id
        task_db = Tasks(**task_data)
        self.db.add(task_db)
        await self.db.commit()
        await self.db.refresh(task_db)

        return task_db

    async def get_all(self, limit, offset) -> List[Tasks]:
        result = await self.db.execute(select(Tasks).limit(limit).offset(offset))
        return list(result.scalars().all())

    async def get_by_id(self, task_id: int) -> Optional[Tasks]:
        result = await self.db.execute(select(Tasks).filter(Tasks.id == task_id))
        return result.scalar_one_or_none()

    async def update(self, task_id: int, task: TaskUpdatingSchema) -> Optional[Tasks]:
        task_db = await self.get_by_id(task_id)

        if not task_db:
            return None

        task_to_update = task.model_dump(exclude_unset=True)

        for field, value in task_to_update.items():
            setattr(task_db, field, value)

        await self.db.commit()
        await self.db.refresh(task_db)

        return task_db

    async def delete(self, task_id: int) -> bool:
        task = await self.get_by_id(task_id)

        if task:
            await self.db.delete(task)
            await self.db.commit()

            return True

        return False
