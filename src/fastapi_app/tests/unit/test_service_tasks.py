from datetime import datetime
from random import randint
from unittest.mock import MagicMock

import pytest
from _pytest.fixtures import fixture

from src.fastapi_app.app.service.task import *
from src.fastapi_app.app.shcemas.task import TaskCreateSchema
from src.fastapi_app.app.shcemas.user import UserDataSchema


@fixture(autouse=True)
def db_mock():
    return MagicMock()


@pytest.mark.parametrize(
    "email, password", [("test1@mail.ru", "1234"), ("test2@mail.ru", "2345")]
)
@pytest.mak.parametrize("text, prior", [("task1", "1"), ("task2", "2"), ("task3", "3")])
def test_task_add(db_mock, email, password, text, prior):
    user = UserDataSchema(email=email, hashed_password=password)
    date = datetime.now()
    task = TaskCreateSchema(user=email, text=text, deadline=date, prior=prior)

    generated_id = randint(0, 100)

    db_mock.create_task.return_value = randint(0, 100)

    id = create_task(user=user, task_data=task, db_client=db_mock)

    assert id
    assert id == generated_id
    db_mock.create_task.assert_called_with(
        user.email, task.text, task.deadline, task.prior
    )


@pytest.mark.parametrize("task_id", ["1", "2"])
def test_delete_task(db_mock, task_id):
    delete_task(task_id, db_mock)
    db_mock.delete_task.assert_called_once_with(task_id)


@pytest.mark.parametrize(
    "user, task_id", [("user1@email.com", "1"), ("user2@email.ru", "2")]
)
def test_get_tasks(db_mock, user, task_id):
    pass


@pytest.mark.parametrize("task_id", ["1", "2"])
def test_complete_task(db_mock, task_id):
    complete_task(task_id, db_mock)
    db_mock.complete_task.assert_called_once_with(task_id)
