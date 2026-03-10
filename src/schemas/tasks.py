from pydantic import BaseModel, Field
from pydantic.types import FutureDate
from typing import Optional, Literal

class BaseTask(BaseModel):
    name: str = Field(max_length=35)
    about: Optional[str] = None
    importance: Literal["Must do", "Should do", "Nice to do", "Optional"]
    responsible: str = Field(min_length=1, strip_whitespace=True)
    deadline: FutureDate
    done: bool = False

class AddTask(BaseTask):
    id: int

class UpdateTask(BaseModel):
    about: str
    done: bool = False