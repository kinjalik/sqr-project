import asyncio
from datetime import datetime
from unittest.mock import MagicMock

import pytest
from _pytest.fixtures import fixture
from app import di
from app.main import app
from app.schemas.user import UserDataSchema
from fastapi.testclient import TestClient


def _db_mock():
    return MagicMock()


@fixture()
def db_mock():
    return _db_mock()


@fixture()
def user():
    return UserDataSchema(email="testTasks@email.com", hashed_password="1234")


@fixture()
def another_user():
    return UserDataSchema(email="test2s@email.com", hashed_password="1234")


@fixture()
def test_client(user):
    tapp = TestClient(app)

    app.dependency_overrides[di.db_client] = _db_mock
    app.state.user = user
    return tapp


@pytest.mark.parametrize("text, prior", [("test1", "1"), ("test2", "2")])
async def test_create_task(user, test_client, text, prior, db_mock):
    date = datetime.now()
    data = {
        "user": user.email,
        "text": text,
        "deadline": date.strftime("%Y.%m.%d %H:%M:%S"),
        "prior": prior,
    }

    response = test_client.post("/task", json=data)

    assert response.status_code == 201
    db_mock.add_task.assert_called_once_with(user.email, text, date, prior)


@pytest.mark.parametrize("task_id", ["1", "2"])
async def test_delete_task(test_client, task_id, db_mock):
    response = test_client.delete(f"/task/{task_id}")
    assert response.status_code == 204
    db_mock.delete_task.assert_called_once_with(task_id)


async def test_get_tasks(user, test_client, db_mock):
    response = test_client.get("/tasks")
    assert response.status_code == 200
    db_mock.get_tasks.assert_called_once_with(user.email)


# TODO: test other methods
