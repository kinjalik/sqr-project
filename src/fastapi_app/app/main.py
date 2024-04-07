"""
Web app setup
"""

from app.auth import router as auth_router
from fastapi import FastAPI


def get_application() -> FastAPI:
    """Get FastAPI web application"""
    application = FastAPI(
        title="SQR",
        version="1.0",
    )

    application.include_router(auth_router, prefix="/auth")

    application.state.token = None

    return application


app = get_application()
