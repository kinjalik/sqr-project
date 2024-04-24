from unittest.mock import MagicMock

import pytest
from _pytest.fixtures import fixture

from src.fastapi_app.app.service.user import *
from src.fastapi_app.app.shcemas.user import UserDataSchema


@fixture(autouse=True)
def db_mock():
    return MagicMock()


@pytest.mark.parametrize(
    "email", "password", [("test1@mail.ru", "1234"), ("test2@mail.ru", "4321")]
)
def test_add_user(db_mock, email, password):
    user = UserDataSchema(email=email, hashed_password=password)
    create_user(user.email, user.hashed_password, db_mock)
    db_mock.add_user.assert_called_once_with(email, password)


@pytest.mark.parametrize(
    "email", "password", [("test1@mail.ru", "1234"), ("test2@mail.ru", "4321")]
)
def test_get_user(db_mock, email, password):
    get_user(email, password, db_mock)
    db_mock.get_user.assert_called_once_with(email, password)
