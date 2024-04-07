"""Auth processing API"""

from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/token")
async def strava_auth_token(request: Request, code: str = ""):
    """Recieve auth token."""
    request.app.state.token = code
