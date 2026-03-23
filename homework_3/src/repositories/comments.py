from typing import List, Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from models import Comments
from schemas import CommentAddingSchema


class CommentsRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create(self, task_id: int, author_id: int, comment: CommentAddingSchema) -> Comments:
        comment_db = Comments(task_id=task_id, author_id=author_id, **comment.model_dump())
        self.db.add(comment_db)
        self.db.commit()
        self.db.refresh(comment_db)

        return comment_db

    def get_by_task_id(self, task_id: int) -> List[Comments]:
        return (
            self.db.query(Comments)
            .filter(Comments.task_id == task_id)
            .order_by(Comments.created_at.asc(), Comments.id.asc())
            .all()
        )

    def get_by_id(self, comment_id: int) -> Optional[Comments]:
        return self.db.query(Comments).filter(Comments.id == comment_id).first()

    def delete(self, comment: Comments) -> None:
        self.db.delete(comment)
        self.db.commit()
