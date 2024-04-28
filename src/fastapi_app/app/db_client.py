import os
from datetime import datetime

from pydantic_settings import BaseSettings
from sqlalchemy import (Boolean, Column, DateTime, Integer, String,
                        create_engine)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String)
    text = Column(String)
    deadline = Column(DateTime)
    prior = Column(Integer)
    is_completed = Column(Boolean, default=False)


class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True)
    hashed_password = Column(String)


class DatabaseConfig(BaseSettings):
    database_url: str = "sqlite:///./test.db"


class DatabaseClient:
    def __init__(self, config: DatabaseConfig):
        self.config = config.database_url
        self.engine = create_engine(self.config)
        self.make_session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def add_task(self, user: str, text: str, deadline: datetime, prior: int):
        with self.make_session() as session:
            new_task = Task(user=user, text=text, deadline=deadline, prior=prior)
            session.add(new_task)
            session.commit()
            return new_task.id

    def add_user(self, email: str, hashed_password: str):
        try:
            with self.make_session() as session:
                new_user = User(email=email, hashed_password=hashed_password)
                session.add(new_user)
                session.commit()
        except IntegrityError as err:
            raise ValueError("User already exist") from err

    def get_tasks(self, user: str):
        with self.make_session() as session:
            return (
                session.query(Task)
                .filter_by(user=user)
                .order_by(Task.prior.desc())
                .all()
            )

    def complete_task(self, task_id: int):
        with self.make_session() as session:
            task = session.query(Task).filter_by(id=task_id).first()
            if task:
                task.is_completed = True
                session.commit()
                return True
            return False

    def get_user(self, email: str, hashed_password: str):
        with self.make_session() as session:
            return (
                session.query(User)
                .filter_by(email=email, hashed_password=hashed_password)
                .first()
            )

    def delete_task(self, task_id: int):
        with self.make_session() as session:
            task = session.query(Task).filter_by(id=task_id).first()
            if task:
                session.delete(task)
                session.commit()
                return True
            return False

    def delete_database(self):
        self.engine.dispose()
        db_file = self.config.replace("sqlite:///", "")

        if os.path.exists(db_file):
            os.remove(db_file)
