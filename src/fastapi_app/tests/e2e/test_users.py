import asyncio
from unittest.mock import MagicMock

import pytest
from _pytest.fixtures import fixture
from app import di
from app.main import app
from fastapi.testclient import TestClient


def _db_mock():
    return MagicMock()


@fixture()
def db_mock():
    return _db_mock()


@fixture(autouse=True)
def test_client():
    tapp = TestClient(app)

    app.dependency_overrides[di.db_client] = _db_mock
    return tapp


@pytest.mark.parametrize(
    "email, password",
    [("test_1@mail.com", "test_passwd1"), ("test_2@mail.ru", "test_passwd2")],
)
async def test_user_register(test_client, email, password, db_mock):
    data = {"email": email, "hashed_password": password}
    response = test_client.post(
        url="/register",
        json=data,
    )

    assert response.status_code == 201

    # TODO: test service level
    assert db_mock.add_user.assert_called_once_with(email, password)
    # TODO try to receive 4x response for duplicate user
    assert response.status_code == 400
    # TODO: test service level
    assert db_mock.add_user.assert_not_called()


@pytest.mark.parametrize(
    "email, password, status_code",
    [("test_1@mail.com", "test_passwd1", 200), ("test_2@mail.ru", "test_passwd3", 404)],
)
async def test_user_login(test_client, email, password, status_code):
    data = {"email": email, "hashed_password": password}
    response = test_client.post(
        url="/login",
        json=data,
    )
    assert response.status_code == status_code
