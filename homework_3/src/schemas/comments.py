from datetime import datetime

from pydantic import BaseModel, Field


class CommentAddingSchema(BaseModel):
    text: str = Field(min_length=1, max_length=300)


class BaseComment(BaseModel):
    id: int
    task_id: int
    author_id: int
    text: str
    created_at: datetime

    model_config = {"from_attributes": True}
