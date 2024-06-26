from unittest.mock import MagicMock

import pytest
from _pytest.fixtures import fixture
from app.schemas.user import UserDataSchema
from app.service.user import create_user, get_user
from app.service.utils import password_hash


@fixture()
def db_mock():
    return MagicMock()


@pytest.mark.parametrize(
    ("email", "password"), [("test1@mail.ru", "1234"), ("test2@mail.ru", "4321")]
)
async def test_add_user(email, password, db_mock):
    user = UserDataSchema(email=email, hashed_password=password)
    await create_user(user.email, user.hashed_password, db_mock)
    db_mock.add_user.assert_called_once()


@pytest.mark.parametrize(
    ("email", "password"), [("test1@mail.ru", "1234"), ("test2@mail.ru", "4321")]
)
async def test_get_user(email, password, db_mock):
    hash = password_hash(str(password))
    db_mock.get_user.return_value = UserDataSchema(email=email, hashed_password=hash)
    await get_user(email, password, db_mock)
    db_mock.get_user.assert_called_once_with(email=email)
