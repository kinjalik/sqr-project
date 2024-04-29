from app.db_client import DatabaseClient
from fastapi import Request


async def db_client(request: Request) -> DatabaseClient:
    return request.app.state.db_client
