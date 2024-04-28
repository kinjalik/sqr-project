import json
from datetime import datetime, timedelta

import pytest
from _pytest.fixtures import fixture
from app import di
from app.db_client import DatabaseClient, DatabaseConfig
from app.main import app
from app.schemas.user import UserDataSchema
from fastapi.testclient import TestClient


@fixture()
def db():
    return DatabaseClient(DatabaseConfig(database_url="sqlite:///./test.db"))


@fixture()
def user():
    return UserDataSchema(email="testTasks@email.com", hashed_password="1234")


@fixture()
def another_user():
    return UserDataSchema(email="test2s@email.com", hashed_password="1234")


@fixture()
def test_client(user, db):
    tapp = TestClient(app)

    app.dependency_overrides[di.db_client] = lambda: db
    app.state.user = user.email
    yield tapp
    db.delete_database()


@pytest.mark.parametrize("text, prior", [("test1", 1), ("test2", 2)])
async def test_create_task(user, test_client, text, prior):
    date = datetime.now().replace(microsecond=0) + timedelta(days=4)
    data = {
        "user": user.email,
        "text": text,
        "deadline": date.strftime("%Y.%m.%d %H:%M:%S"),
        "prior": prior,
    }

    response = test_client.post("/task", json=data)

    assert response.status_code == 201
    print(response.content)
    print(json.loads(response.content)["task_id"])
    assert json.loads(response.content)["task_id"]


@pytest.mark.parametrize("text, prior", [("test1", 1), ("test2", 2)])
async def test_delete_task(user, test_client, text, prior):
    date = datetime.now().replace(microsecond=0) + timedelta(days=4)

    data = {
        "user": user.email,
        "text": text,
        "deadline": date.strftime("%Y.%m.%d %H:%M:%S"),
        "prior": prior,
    }

    response = test_client.post("/task", json=data)
    assert response.status_code == 201
    task_id = json.loads(response.content)["task_id"]
    assert task_id

    response = test_client.delete(f"/task/{task_id}")
    assert response.status_code == 204

    response = test_client.delete(f"/task/{task_id}")
    assert response.status_code == 404


@pytest.mark.parametrize("text, prior", [("test1", 1), ("test2", 2)])
async def test_get_tasks(user, test_client, text, prior):
    date = datetime.now().replace(microsecond=0) + timedelta(days=4)

    data = {
        "user": user.email,
        "text": text,
        "deadline": date.strftime("%Y.%m.%d %H:%M:%S"),
        "prior": prior,
    }

    response = test_client.post("/task", json=data)
    assert response.status_code == 201
    task_id = json.loads(response.content)["task_id"]
    assert task_id

    response = test_client.get("/tasks")
    assert response.status_code == 200
    serialized_json = json.loads(response.content)

    assert serialized_json["tasks"]
    assert len(serialized_json["tasks"]) == 1
    for data in serialized_json["tasks"]:
        assert data["id"]
        assert data["id"] == task_id
        assert data["user"]
        assert data["deadline"]
        assert data["prior"]
        assert not data["is_completed"]


@pytest.mark.parametrize("text, prior", [("test1", 1), ("test2", 2)])
async def test_complete_task(user, test_client, text, prior):
    date = datetime.now().replace(microsecond=0) + timedelta(days=4)

    data = {
        "user": user.email,
        "text": text,
        "deadline": date.strftime("%Y.%m.%d %H:%M:%S"),
        "prior": prior,
    }

    response = test_client.post("/task", json=data)
    assert response.status_code == 201
    task_id = json.loads(response.content)["task_id"]
    assert task_id

    response = test_client.get("/tasks")
    assert response.status_code == 200
    serialized_json = json.loads(response.content)

    assert serialized_json["tasks"]
    assert len(serialized_json["tasks"]) == 1
    for data in serialized_json["tasks"]:
        assert data["id"]
        if data["id"] == task_id:
            assert not data["is_completed"]

    response = test_client.put(f"/task/{task_id+1}/complete")
    assert response.status_code == 404

    response = test_client.put(f"/task/{task_id}/complete")
    assert response.status_code == 204

    response = test_client.get("/tasks")
    assert response.status_code == 200
    serialized_json = json.loads(response.content)

    assert serialized_json["tasks"]
    assert len(serialized_json["tasks"]) == 1
    for data in serialized_json["tasks"]:
        assert data["id"]
        if data["id"] == task_id:
            assert data["is_completed"]


@pytest.mark.parametrize("text, prior", [("test1", 1), ("test2", 2)])
async def test_edit_task(user, test_client, text, prior):
    date = datetime.now().replace(microsecond=0) + timedelta(days=4)

    data = {
        "user": user.email,
        "text": text,
        "deadline": date.strftime("%Y.%m.%d %H:%M:%S"),
        "prior": prior,
    }

    response = test_client.post("/task", json=data)
    assert response.status_code == 201
    task_id = json.loads(response.content)["task_id"]
    assert task_id

    new_data = {
        "text": data["text"] + "NEW_TEXT",
        "deadline": data["deadline"],
        "prior": data["prior"] + 1,
    }
    response = test_client.put(f"/task/{task_id}", json=new_data)
    assert response.status_code == 204

    response = test_client.get("/tasks")
    assert response.status_code == 200
    serialized_json = json.loads(response.content)

    assert serialized_json["tasks"]
    assert len(serialized_json["tasks"]) == 1
    for response_data in serialized_json["tasks"]:
        assert response_data["id"] is not None
        assert response_data["id"] == task_id

        assert response_data["text"] is not None
        assert response_data["text"] == new_data["text"]

        assert response_data["deadline"] is not None
        assert response_data["deadline"] == new_data["deadline"]

        assert response_data["prior"] is not None
        assert response_data["prior"] == new_data["prior"]
