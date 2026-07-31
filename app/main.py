from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlmodel import Session, select

from app.database import create_db_and_tables, get_session
from app.models import Task, TaskCreate, TaskPublic, TaskUpdate


SessionDependency = Annotated[
    Session,
    Depends(get_session),
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create the database tables when the application starts."""
    create_db_and_tables()
    yield


app = FastAPI(
    title="Developer Workspace Assistant",
    description="An API for managing developer tasks and workspace tools.",
    version="0.4.0",
    lifespan=lifespan,
)


@app.get("/",
          operation_id="read_root",
         )
def read_root() -> dict[str, str]:
    """Return basic information about the application."""
    return {
        "message": "Developer Workspace Assistant is running",
        "version": "0.4.0",
    }


@app.get("/health",
    operation_id="health_check",
    )
def health_check() -> dict[str, str]:
    """Return the current health status."""
    return {"status": "healthy"}


@app.post(
    "/tasks",
    response_model=TaskPublic,
    status_code=status.HTTP_201_CREATED,
    operation_id="create_task",
)
def create_task(
    *,
    session: SessionDependency,
    task_data: TaskCreate,
) -> Task:
    """Create and store a new task."""

    database_task = Task.model_validate(task_data)

    session.add(database_task)
    session.commit()
    session.refresh(database_task)

    return database_task


@app.get(
    "/tasks",
    response_model=list[TaskPublic],
    operation_id="list_tasks",
)
def list_tasks(
    *,
    session: SessionDependency,
    offset: int = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> list[Task]:
    """Return stored tasks using pagination."""

    statement = (
        select(Task)
        .offset(offset)
        .limit(limit)
    )

    return list(session.exec(statement).all())


@app.get(
    "/tasks/{task_id}",
    response_model=TaskPublic,
    operation_id="get_task",
)
def get_task(
    *,
    session: SessionDependency,
    task_id: int,
) -> Task:
    """Return one task using its identifier."""

    task = session.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} was not found.",
        )

    return task


@app.patch(
    "/tasks/{task_id}",
    response_model=TaskPublic,
    operation_id="update_task",
)
def update_task(
    *,
    session: SessionDependency,
    task_id: int,
    task_data: TaskUpdate,
) -> Task:
    """Partially update a stored task."""

    database_task = session.get(Task, task_id)

    if database_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} was not found.",
        )

    updated_fields = task_data.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    database_task.sqlmodel_update(updated_fields)

    session.add(database_task)
    session.commit()
    session.refresh(database_task)

    return database_task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="delete_task",
)
def delete_task(
    *,
    session: SessionDependency,
    task_id: int,
) -> Response:
    """Delete a stored task."""

    database_task = session.get(Task, task_id)

    if database_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} was not found.",
        )

    session.delete(database_task)
    session.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )