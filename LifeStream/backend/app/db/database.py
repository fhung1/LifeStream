"""Database connection and session management."""
from sqlalchemy import create_engine, pool
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Generator

from app.core.config import settings
from app.db.base import Base


# Create engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=pool.QueuePool,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,  # Verify connections before using
    echo=settings.DB_ECHO,  # Log SQL queries in debug mode
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def init_db() -> None:
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    Database session context manager.
    
    Usage:
        with get_db() as db:
            # use db session
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_db_session() -> Session:
    """
    Get a database session (for dependency injection).
    
    Usage:
        db = get_db_session()
        try:
            # use db session
        finally:
            db.close()
    """
    return SessionLocal()
