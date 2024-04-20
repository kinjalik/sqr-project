from typing import List

from app.db_client import DatabaseClient
from app.shcemas.task import TaskCreateSchema, TaskModel


async def create_task(task_data: TaskCreateSchema, db_client: DatabaseClient):
    pass


async def delete_task(task_id: str, db_client: DatabaseClient):
    pass


async def complete_task(task_id: str, db_client: DatabaseClient):
    pass


async def get_tasks(user: str, db_client: DatabaseClient) -> List[TaskModel]:
    pass
