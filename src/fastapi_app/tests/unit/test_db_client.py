from datetime import datetime, timedelta

import pytest
from app.db_client import DatabaseClient, DatabaseConfig
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

EMAIL = "email"
HASHED_PASSWORD = "hashed_password"

ID = "id"
USER = "user"
TEXT = "text"
DEADLINE = "deadline"
PRIOR = "prior"
IS_COMPETED = "is_completed"


@pytest.fixture
def db_client():
    config = DatabaseConfig(database_url="sqlite:///:memory:")
    client = DatabaseClient(config=config)
    return client


@pytest.fixture
def db_session(db_client):
    make_session = sessionmaker(bind=db_client.engine)
    session = make_session()
    yield session
    session.close()


@pytest.fixture
def credo_user1():
    return {
        EMAIL: "aboba@innopolis.univeristy",
        HASHED_PASSWORD: "my_strong_password228",
    }


@pytest.fixture
def credo_task1():
    return {
        TEXT: "SomeTestText",
        DEADLINE: datetime.now() + timedelta(days=4),
        PRIOR: 4,
        IS_COMPETED: False,
    }


def get_user_raw_sql(db_session, credo_user):
    sql_query = text(f"SELECT * FROM users WHERE {EMAIL} = :{EMAIL}")
    result = db_session.execute(sql_query, {EMAIL: credo_user[EMAIL]}).fetchone()
    return result


def add_user_raw_sql(db_session, credo_user):
    sql = text(
        f"INSERT INTO users ({EMAIL}, {HASHED_PASSWORD}) "
        f"VALUES (:{EMAIL}, :{HASHED_PASSWORD})"
    )
    db_session.execute(
        sql, {EMAIL: credo_user[EMAIL], HASHED_PASSWORD: credo_user[HASHED_PASSWORD]}
    )
    db_session.commit()


def get_task_raw_sql(db_session, task_id):
    sql = text(f"SELECT * FROM tasks WHERE {ID} = :{ID}")
    return db_session.execute(sql, {ID: task_id}).fetchone()


def add_task_raw_sql(db_session, user, new_text, deadline, prior, is_completed=False):
    sql = text(
        f"INSERT INTO tasks ({USER}, {TEXT}, {DEADLINE}, {PRIOR}, {IS_COMPETED}) "
        f"VALUES (:{USER}, :{TEXT}, :{DEADLINE}, :{PRIOR}, :{IS_COMPETED})"
    )
    db_session.execute(
        sql,
        {
            USER: user,
            TEXT: new_text,
            DEADLINE: deadline,
            PRIOR: prior,
            IS_COMPETED: is_completed,
        },
    )
    db_session.commit()

    result = db_session.execute(text("SELECT last_insert_rowid()"))
    return result.fetchone()[0]


async def test_add_user(db_client, db_session, credo_user1):
    db_client.add_user(credo_user1[EMAIL], credo_user1[HASHED_PASSWORD])

    result = get_user_raw_sql(db_session, credo_user1)

    assert result is not None
    assert result[0] == credo_user1[EMAIL]
    assert result[1] == credo_user1[HASHED_PASSWORD]


async def test_add_task(db_client, db_session, credo_user1):
    new_text = "TEST_TEXT"
    deadline = datetime.now() + timedelta(days=228)
    prior = 882

    add_user_raw_sql(db_session, credo_user1)
    task_id = db_client.add_task(credo_user1[EMAIL], new_text, deadline, prior)
    result = get_task_raw_sql(db_session, task_id)

    assert result is not None
    assert result[1] == credo_user1[EMAIL]
    assert result[2] == new_text
    assert result[3] == str(deadline)
    assert result[4] == prior
    assert not result[5]


async def test_complete_task(db_client, db_session, credo_user1):
    is_complete = db_client.complete_task(777)
    assert is_complete is not None
    assert is_complete is False

    new_text = "SHOULD BE DONE"
    deadline = datetime.now() + timedelta(days=4)
    prior = 2

    add_user_raw_sql(db_session, credo_user1)
    task_id = add_task_raw_sql(
        db_session, credo_user1[EMAIL], new_text, deadline, prior
    )

    is_complete = db_client.complete_task(task_id)
    assert is_complete is not None
    assert is_complete is True

    result = get_task_raw_sql(db_session, task_id)

    assert result is not None
    assert result[5]


async def test_get_task(db_client, db_session, credo_user1):
    new_text = "SOME TEXT"
    deadline = datetime.now()
    prior = 4
    add_user_raw_sql(db_session, credo_user1)
    add_task_raw_sql(db_session, credo_user1[EMAIL], new_text, deadline, prior)

    tasks = db_client.get_tasks(credo_user1[EMAIL])

    assert tasks is not None
    assert len(tasks) == 1
    assert tasks[0].user == credo_user1[EMAIL]
    assert tasks[0].text == new_text
    assert tasks[0].deadline == deadline
    assert tasks[0].prior == prior
    assert not tasks[0].is_completed


async def test_get_user(db_client, db_session, credo_user1):
    maybe_user = db_client.get_user(credo_user1[EMAIL], credo_user1[HASHED_PASSWORD])
    assert maybe_user is None
    add_user_raw_sql(db_session, credo_user1)
    maybe_user = db_client.get_user(credo_user1[EMAIL], credo_user1[HASHED_PASSWORD])
    assert maybe_user is not None
    assert maybe_user.email == credo_user1[EMAIL]
    assert maybe_user.hashed_password == credo_user1[HASHED_PASSWORD]


async def test_delete_task(db_client, db_session, credo_user1, credo_task1):
    is_delete = db_client.delete_task(777)
    assert is_delete is not None
    assert is_delete is False

    add_user_raw_sql(db_session, credo_user1)
    task_id = add_task_raw_sql(
        db_session,
        credo_user1[EMAIL],
        credo_task1[TEXT],
        credo_task1[DEADLINE],
        credo_task1[PRIOR],
        credo_task1[IS_COMPETED],
    )
    return_task = get_task_raw_sql(db_session, task_id)
    assert return_task is not None

    is_delete = db_client.delete_task(task_id)
    assert is_delete is not None
    assert is_delete is True

    return_task = get_task_raw_sql(db_session, task_id)
    assert return_task is None
