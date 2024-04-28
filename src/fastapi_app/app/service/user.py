from app.db_client import DatabaseClient
from app.service.utils import password_hash, password_verification


async def create_user(email: str, hashed_password: str, db_client: DatabaseClient):
    hashed_password = password_hash(hashed_password)
    db_client.add_user(email, hashed_password)


async def get_user(email: str, hashed_password: str, db_client: DatabaseClient) -> str:
    user = db_client.get_user(email=email)
    if user is None or not password_verification(hashed_password, user.hashed_password):
        raise ValueError
    return user.email
