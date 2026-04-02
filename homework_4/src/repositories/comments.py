from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models import Comments
from schemas import CommentAddingSchema


class CommentsRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create(self, task_id: int, author_id: int, comment: CommentAddingSchema) -> Comments:
        comment_db = Comments(task_id=task_id, author_id=author_id, **comment.model_dump())
        self.db.add(comment_db)
        await self.db.commit()
        await self.db.refresh(comment_db)

        return comment_db

    async def get_by_task_id(self, task_id: int) -> List[Comments]:
        result = await self.db.execute(
            select(Comments)
            .filter(Comments.task_id == task_id)
            .order_by(Comments.created_at.asc(), Comments.id.asc())
        )
        return list(result.scalars().all())

    async def get_by_id(self, comment_id: int) -> Optional[Comments]:
        result = await self.db.execute(select(Comments).filter(Comments.id == comment_id))
        return result.scalar_one_or_none()

    async def delete(self, comment: Comments) -> None:
        await self.db.delete(comment)
        await self.db.commit()
