from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

from src.core.config import get_settings


class Base(DeclarativeBase):
    """SQLAlchemy declarative base."""
    pass


def _create_engine_from_settings():
    settings = get_settings()
    database_url = settings.DATABASE_URL

    # SQLite needs special connect args
    connect_args = {}
    if database_url.startswith("sqlite"):
        # check_same_thread False for use in FastAPI sync endpoints within same process
        connect_args = {"check_same_thread": False}

    engine = create_engine(
        database_url,
        echo=False,
        future=True,
        pool_pre_ping=True,
        connect_args=connect_args,
    )
    return engine


engine = _create_engine_from_settings()

# Configure session factory
SessionLocal = sessionmaker(
    bind=engine, autocommit=False, autoflush=False, expire_on_commit=False, class_=Session
)


# PUBLIC_INTERFACE
def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a SQLAlchemy Session and ensures it's closed."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# PUBLIC_INTERFACE
def init_db() -> None:
    """Initialize database by creating all tables if they don't exist."""
    # Import models so that metadata is populated
    from src.db import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
