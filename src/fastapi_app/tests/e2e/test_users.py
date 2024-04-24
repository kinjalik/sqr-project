from unittest.mock import MagicMock

import pytest
from _pytest.fixtures import fixture
from app import di
from app.main import app
from app.shcemas.user import UserDataSchema
from fastapi.testclient import TestClient


@fixture(autouse=True)
def db_mock():
    return MagicMock()


@fixture(autouse=True)
def test_client(db_mock):
    tapp = TestClient(app)

    app.dependency_overrides[di.db_client] = db_mock
    return tapp


@pytest.mark.parametrize(
    "email, password",
    [("test_1@mail.com", "test_passwd1"),
     ("test_2@mail.ru", "test_passwd2")],
)
def test_user_register(test_client, email, password):
    print(UserDataSchema(email=email, hashed_password=password).__dict__)
    response = test_client.post(
        url="/register",
        data=UserDataSchema(email=email, hashed_password=password).__dict__,
    )
    assert response.status_code == 201
    assert not len(response.content.hex())
    # TODO: test serviceLevel
    assert db_mock.add_user.assert_called_once_with(email, password)
    # TODO try to receive 4x response for duplicate user
    assert response.status_code == 400
    # TODO: test serviceLevel
    assert db_mock.add_user.assert_not_called()


@pytest.mark.parametrize(
    "email, password, status_code",
    [("test_1@mail.com", "test_passwd1", 200),
     ("test_2@mail.ru", "test_passwd3", 404)],
)
def test_user_login(test_client, email, password, status_code):
    response = test_client.post(
        url="/login",
        data=UserDataSchema(email=email, hashed_password=password).__dict__,
    )
    assert response.status_code == status_code
    assert not len(response.content.hex())
