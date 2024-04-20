from datetime import datetime
from unittest.mock import MagicMock

import pytest
from _pytest.fixtures import fixture
from app import di
from app.main import app
from fastapi.testclient import TestClient

from src.fastapi_app.app.shcemas.task import TaskCreateSchema
from src.fastapi_app.app.shcemas.user import UserDataSchema


@fixture(autouse=True)
def db_mock():
    return MagicMock()


@fixture(autouse=True)
def user():
    return UserDataSchema("testTasks@email.com", "1234")


@fixture(autouse=True)
def another_user():
    return UserDataSchema("testTasks2@email.com", "4321")


@fixture(autouse=True)
def test_client(db_mock, user):
    tapp = TestClient(app)

    app.dependency_overrides[di.db_client] = db_mock
    app.state.user = user
    return tapp


@pytest.mark.parametrize("text, prior", [("test1", "1"), ("test2", "2")])
def test_create_task(db_mock, user, test_client, text, prior):
    date = datetime.now()

    task = TaskCreateSchema(user=user.email, text=text,
                            deadline=date, prior=prior)
    response = test_client.post("/task", data=task.dict)

    assert response.status_code == 201
    db_mock.add_task.assert_called_once_with(user.email, text, date, prior)


@pytest.mark.parametrize("task_id", ["1", "2"])
def test_delete_task(db_mock, test_client, task_id):
    response = test_client.delete("/task", json={"id": task_id})
    assert response.status_code == 204
    db_mock.delete_task.assert_called_once_with(task_id)


def test_get_tasks(db_mock):
    response = test_client.get("/task")
    assert response.status_code == 200
    db_mock.get_tasks.assert_called_once_with(user.email)


# TODO: test other methods
