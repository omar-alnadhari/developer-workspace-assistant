import os
from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///tasks.db",
)

connect_args = (
    {"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=True,
)


def create_db_and_tables() -> None:
    """Create database tables that do not already exist."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Provide one database session for each API request."""
    with Session(engine) as session:
        yield session