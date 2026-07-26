from sqlmodel import Field, SQLModel


class TaskBase(SQLModel):
    """Fields shared by task models."""

    title: str = Field(
        min_length=1,
        max_length=100,
        index=True,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    completed: bool = False


class Task(TaskBase, table=True):
    """Database table representing stored tasks."""

    id: int | None = Field(
        default=None,
        primary_key=True,
    )


class TaskCreate(TaskBase):
    """Data accepted when creating a task."""

    pass


class TaskPublic(TaskBase):
    """Data returned to API clients."""

    id: int


class TaskUpdate(SQLModel):
    """Optional fields accepted during partial updates."""

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    completed: bool | None = None