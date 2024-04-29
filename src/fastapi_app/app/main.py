# pylint: disable=redefined-outer-name
"""
Web app setup
"""

import typing as t

from app.api.health import router as healthcheck_api
from app.api.task import router as task_api
from app.api.user import router as user_api
from app.db_client import DatabaseClient, DatabaseConfig
from fastapi import FastAPI


def create_start_app_handler(
    app: FastAPI,
) -> t.Callable[[], t.Coroutine[None, None, None]]:
    """On startup event function"""

    async def start_app() -> None:
        db_client = DatabaseClient(DatabaseConfig())

        app.state.db_client = db_client
        app.state.user = None

    return start_app


def get_application() -> FastAPI:
    """Get FastAPI web application"""
    application = FastAPI(
        title="SQR",
        version="1.0",
    )

    application.add_event_handler("startup", create_start_app_handler(application))

    application.include_router(task_api)
    application.include_router(user_api)
    application.include_router(healthcheck_api)

    return application


app = get_application()
