from app import di
from app.db_client import DatabaseClient
from app.schemas.user import UserDataSchema
from app.service import user as service
from fastapi import APIRouter, Depends, Request, Response, responses

router = APIRouter()


@router.post(
    "/register",
)
async def register(
    user_create_data: UserDataSchema,
    db_client: DatabaseClient = Depends(di.db_client),
):
    try:
        await service.create_user(
            user_create_data.email,
            user_create_data.hashed_password,
            db_client=db_client,
        )
    except ValueError:
        return responses.JSONResponse(
            status_code=400, content={"error": "this user is already registered"}
        )

    return Response(status_code=201)


@router.post(
    "/login",
)
async def login(
    user_data: UserDataSchema,
    request: Request,
    db_client: DatabaseClient = Depends(di.db_client),
):
    try:
        request.app.state.user = await service.get_user(
            user_data.email, user_data.hashed_password, db_client=db_client
        )
    except ValueError:
        return responses.JSONResponse(
            status_code=404, content={"error": "the user was not found"}
        )

    return Response(status_code=200)
