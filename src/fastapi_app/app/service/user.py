from app.db_client import DatabaseClient
from app.utils import password_hash


async def create_user(email: str, hashed_password: str, db_client: DatabaseClient):
    hashed_password = password_hash(hashed_password)
    db_client.add_user(email, hashed_password)


async def get_user(email: str, hashed_password: str, db_client: DatabaseClient) -> str:
    user = db_client.get_user(email=email)
    if user is None:
        raise ValueError
    user.hashed_password[:16]
    return user.email
