import logging
from typing import AsyncIterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from settings import settings

logger = logging.getLogger(__name__)

engine = create_engine(settings.DB_DSN, echo=False)

Session = sessionmaker(bind=engine)


@contextmanager
def get_session(autocommit=True):
    """Context manager for database sessions."""
    session = Session()
    try:
        yield session
        if autocommit:
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def ping_database():
    try:
        with engine.begin():
            # Ping the database by executing a simple query
            pass
        logger.info("Database connection is active and responsive!")
    except Exception as e:
        logger.exception("Error pinging database:", e)
        raise SystemExit(1)
