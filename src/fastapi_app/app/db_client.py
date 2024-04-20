from pydantic_settings import BaseSettings
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String)
    text = Column(String)
    deadline = Column(DateTime)
    prior = Column(Integer)
    is_completed = Column(Boolean, default=False)

    def __repr__(self):
        return (f"Task("
                f"id={self.id}, "
                f"User='{self.user}', "
                f"Text='{self.text}', "
                f"Deadline='{self.deadline}', "
                f"Priority='{self.prior}', "
                f"Completed={self.is_completed})")


class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True)
    hashed_password = Column(String)


class DatabaseConfig(BaseSettings):
    database_url: str = "sqlite:///./test.db"


class DatabaseClient:
    def __init__(self, config: DatabaseConfig):
        self.engine = create_engine(config.database_url)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def add_task(self, user: str, text: str, deadline: datetime, prior: int):
        with self.Session() as session:
            new_task = Task(user=user, text=text, deadline=deadline, prior=prior)
            session.add(new_task)
            session.commit()
            return new_task.id

    def add_user(self, email: str, hashed_password: str):
        with self.Session() as session:
            new_user = User(email=email, hashed_password=hashed_password)
            session.add(new_user)
            session.commit()

    def get_tasks(self, user: str):
        with self.Session() as session:
            return session.query(Task).filter_by(user=user).all()

    def complete_task(self, task_id: int):
        with self.Session() as session:
            task = session.query(Task).filter_by(id=task_id).first()
            if task:
                task.is_completed = True
                session.commit()


def print_all_tasks(db_client, user):
    tasks = db_client.get_tasks(user)
    for task in tasks:
        print(task)


if __name__ == "__main__":
    config = DatabaseConfig(database_url="sqlite:///:memory:")
    db_client = DatabaseClient(config)

    email = "aboba@innopolis.university"
    db_client.add_user(email=email, hashed_password="hashed_pass")

    id_task = db_client.add_task(user=email, text="I LOVE SQR", deadline=datetime.now(), prior=1)
    print(f'New id: {id_task}')
    tasks = db_client.get_tasks(user=email)

    print_all_tasks(db_client, email)
