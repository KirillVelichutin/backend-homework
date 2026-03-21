from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import date

class BaseTask(BaseModel):
    id: int
    name: str = Field(max_length=35)
    about: Optional[str] = None
    importance: Literal["Must do", "Should do", "Nice to do", "Optional"]
    responsible_id: int
    deadline: date
    is_done: bool = False

class TaskAddingSchema(BaseModel):
    name: str = Field(max_length=35)
    about: Optional[str] = None
    importance: Literal["Must do", "Should do", "Nice to do", "Optional"]
    responsible_id: int
    deadline: date
    is_done: bool = False
    

class TaskUpdatingSchema(BaseModel):
    about: str
    is_done: bool