from app.db_client import DatabaseClient


async def create_user(email: str, hashed_password: str, db_client: DatabaseClient):
    db_client.add_user(email, hashed_password)


async def get_user(email: str, hashed_password: str, db_client: DatabaseClient) -> str:
    return db_client.get_user(email=email, hashed_password=hashed_password)
