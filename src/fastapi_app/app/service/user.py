from app.db_client import DatabaseClient


async def create_user(email: str, hashed_password: str, db_client: DatabaseClient):
    pass


async def get_user(email: str, hashed_password: str, db_client: DatabaseClient) -> str:
    pass
