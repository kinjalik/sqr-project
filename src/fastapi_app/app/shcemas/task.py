from datetime import datetime

from pydantic import BaseModel


class TaskCreateSchema(BaseModel):
    user: str
    text: str
    deadline: datetime
    prior: int


class TaskModel(TaskCreateSchema):
    id: str
    is_completed: bool = False
