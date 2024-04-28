from datetime import datetime
from random import randint
from unittest.mock import MagicMock

import pytest
from _pytest.fixtures import fixture
from app.schemas.task import TaskCreateSchema, TaskEditSchema
from app.schemas.user import UserDataSchema
from app.service.task import complete_task, create_task, delete_task, edit_task


@fixture()
def db_mock():
    return MagicMock()


@pytest.mark.parametrize(
    ("email, password"), [("test1@mail.ru", "1234"), ("test2@mail.ru", "2345")]
)
@pytest.mark.parametrize(
    "text, prior", [("task1", "1"), ("task2", "2"), ("task3", "3")]
)
async def test_task_add(email, password, text, prior, db_mock):
    user = UserDataSchema(email=email, hashed_password=password)
    date = datetime.now()
    task = TaskCreateSchema(
        user=email, text=text, deadline=date.strftime("%Y.%m.%d %H:%M:%S"), prior=prior
    )

    generated_id = randint(0, 100)

    db_mock.add_task.return_value = generated_id

    id = await create_task(task_data=task, db_client=db_mock)

    assert id is not None
    assert id == generated_id
    db_mock.add_task.assert_called_with(
        user.email,
        task.text,
        datetime.strptime(task.deadline, "%Y.%m.%d %H:%M:%S"),
        task.prior,
    )


@pytest.mark.parametrize("task_id", ["1", "2"])
async def test_delete_task(task_id, db_mock):
    await delete_task(task_id, db_mock)
    db_mock.delete_task.assert_called_once_with(task_id)


@pytest.mark.parametrize(
    ("user, task_id"), [("user1@email.com", "1"), ("user2@email.ru", "2")]
)
async def test_get_tasks(user, task_id, db_mock):
    pass


@pytest.mark.parametrize("task_id", ["1", "2"])
async def test_complete_task(task_id, db_mock):
    await complete_task(task_id, db_mock)
    db_mock.complete_task.assert_called_once_with(task_id)


@pytest.mark.parametrize(("task_id"), [(1), (2)])
@pytest.mark.parametrize(
    "text, prior", [("task1", "1"), ("task2", "2"), ("task3", "3")]
)
async def test_task_edit(task_id, text, prior, db_mock):
    date = datetime.now()
    task = TaskEditSchema(
        text=text, deadline=date.strftime("%Y.%m.%d %H:%M:%S"), prior=prior
    )
    await edit_task(task_id=task_id, task_data=task, db_client=db_mock)
    db_mock.edit_task.assert_called_once_with(
        task_id,
        task.text,
        datetime.strptime(task.deadline, "%Y.%m.%d %H:%M:%S"),
        task.prior,
    )
