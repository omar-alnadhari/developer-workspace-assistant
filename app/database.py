from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine


DATABASE_FILE = "tasks.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

connect_args = {
    "check_same_thread": False,
}

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