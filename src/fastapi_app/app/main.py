"""
Web app setup
"""

from fastapi import FastAPI


def get_application() -> FastAPI:
    """Get FastAPI web application"""
    application = FastAPI(
        title="SQR",
        version="1.0",
    )

    return application


app = get_application()
