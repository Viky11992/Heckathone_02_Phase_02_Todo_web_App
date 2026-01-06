from sqlmodel import create_engine, Session
from typing import Generator
from contextlib import contextmanager
import os
from config import settings


# Create the database engine
engine = create_engine(
    settings.database_url,
    echo=settings.db_echo,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=0
)


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session
    """
    with Session(engine) as session:
        yield session


@contextmanager
def get_db_session():
    """
    Context manager for database sessions
    """
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()