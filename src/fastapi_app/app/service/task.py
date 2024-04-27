from typing import List

from app.db_client import DatabaseClient
from app.schemas.task import TaskCreateSchema, TaskModel


async def create_task(task_data: TaskCreateSchema, db_client: DatabaseClient):
    return db_client.create_task(
        # TODO: parse deadline from str format (%Y.%m.%d %H:%M:%S) to datetime ??
        task_data.user,
        task_data.text,
        task_data.deadline,
        task_data.prior,
    )


async def delete_task(task_id: str, db_client: DatabaseClient):
    return db_client.delete_task(task_id)


async def complete_task(task_id: str, db_client: DatabaseClient):
    db_client.complete_task(task_id)


async def get_tasks(user: str, db_client: DatabaseClient) -> List[TaskModel]:
    return db_client.get_tasks(user)
