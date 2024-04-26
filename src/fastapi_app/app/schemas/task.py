from pydantic import BaseModel


class TaskCreateSchema(BaseModel):
    user: str
    text: str
    deadline: str
    prior: int


class TaskModel(TaskCreateSchema):
    id: str
    is_completed: bool = False
