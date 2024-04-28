import pytest
from _pytest.fixtures import fixture
from app import di
from app.db_client import Base, DatabaseClient, DatabaseConfig
from app.main import app
from fastapi.testclient import TestClient


@fixture(autouse=True)
def db():
    client = DatabaseClient(DatabaseConfig(database_url="sqlite:///./test.db"))
    return client


@fixture(autouse=True)
def test_client(db):
    tapp = TestClient(app)

    app.dependency_overrides[di.db_client] = lambda: db
    yield tapp
    db.delete_database()


@pytest.mark.parametrize(
    "email, password",
    [("test_1@mail.com", "test_passwd1"), ("test_2@mail.ru", "test_passwd2")],
)
async def test_user_register(test_client, email, password):
    data = {"email": email, "hashed_password": password}
    response = test_client.post(
        url="/register",
        json=data,
    )

    assert response.status_code == 201

    response = test_client.post(
        url="/register",
        json=data,
    )

    assert response.status_code == 400


@pytest.mark.parametrize(
    "email, password, status_code",
    [("test_1@mail.com", "test_passwd1", 200), ("test_2@mail.ru", "test_passwd3", 200)],
)
async def test_user_login(test_client, email, password, status_code):
    data = {"email": email, "hashed_password": password}
    response = test_client.post(
        url="/register",
        json=data,
    )
    assert response.status_code == 201

    data = {"email": email, "hashed_password": password}
    response = test_client.post(
        url="/login",
        json=data,
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code",
    [("test_1@mail.com", "test_passwd1", 404), ("test_2@mail.ru", "test_passwd3", 404)],
)
async def test_user_login_without_registration(
    test_client, email, password, status_code
):
    data = {"email": email, "hashed_password": password}
    response = test_client.post(
        url="/login",
        json=data,
    )
    assert response.status_code == status_code
