from app import di
from app.db_client import DatabaseClient
from app.service import task as service
from app.shcemas.task import TaskCreateSchema
from fastapi import APIRouter, Depends, Request, Response, responses

router = APIRouter()


@router.post(
    "/task",
)
async def create_task(
    task_create_data: TaskCreateSchema,
    request: Request,
    db_client: DatabaseClient = Depends(di.db_client),
):
    try:
        await service.create_task(
            task_data=task_create_data,
            db_client=db_client,
        )
    except ValueError:
        return Response(status_code=400, content={"error": "the user was not found"})

    return Response(status_code=201)


@router.delete(
    "/task",
)
async def delete_task(
    id: str,
    db_client: DatabaseClient = Depends(di.db_client),
):
    try:
        await service.delete_task(
            task_id=id,
            db_client=db_client,
        )
    except ValueError:
        return Response(status_code=404, content={"error": "the task was not found"})

    return Response(status_code=204)


@router.get(
    "/tasks",
)
async def get_tasks(
    request: Request,
    db_client: DatabaseClient = Depends(di.db_client),
):
    try:
        await service.get_tasks(
            user=request.app.state.user,
            db_client=db_client,
        )
    except ValueError:
        return Response(status_code=404, content={"error": "the user was not found"})

    return responses.JSONResponse(content={})


@router.put(
    "/task/{id}/complete",
)
async def complete_task(
    id: str,
    db_client: DatabaseClient = Depends(di.db_client),
):
    try:
        await service.complete_task(
            task_id=id,
            db_client=db_client,
        )
    except ValueError:
        return Response(status_code=404, content={"error": "the task was not found"})

    return Response(status_code=204)
