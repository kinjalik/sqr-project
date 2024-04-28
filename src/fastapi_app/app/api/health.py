from fastapi import APIRouter, Response

router = APIRouter()


@router.get(
    "/health",
)
async def healthcheck():
    return Response(status_code=200, content="ok")
