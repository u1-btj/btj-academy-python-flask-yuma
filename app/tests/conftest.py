from typing import Generator

import pytest
from httpx import Client
from sqlalchemy import create_engine, event, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from db import Session
from main import app
from models.base import Base
from settings import settings

SPLITS = settings.DB_DSN.split("/")
DSN = "/".join(SPLITS[:len(SPLITS)-1])

@pytest.fixture
def client() -> Generator:
    with Client(app=app, base_url="https://test") as c:
        yield c


@pytest.fixture(scope="session")
def setup_db() -> Generator:
    engine = create_engine(f"{DSN}")
    conn = engine.connect()
    # Terminate transaction
    conn.execute(text("commit"))
    try:
        conn.execute(text(f"drop database {settings.DB_NAME}"))
    except SQLAlchemyError:
        pass
    finally:
        conn.close()

    conn = engine.connect()
    # Terminate transaction
    conn.execute(text("commit"))
    conn.execute(text(f"create database {settings.DB_NAME}"))
    conn.close()

    yield

    conn = engine.connect()
    # Terminate transaction
    conn.execute(text("commit"))
    try:
        conn.execute(text(f"drop database {settings.DB_NAME}"))
    except SQLAlchemyError:
        pass
    conn.close()
    engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def setup_test_db(setup_db: Generator) -> Generator:
    engine = create_engine(settings.DB_DSN)

    with engine.begin():
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        yield
        Base.metadata.drop_all(engine)

    engine.dispose()


@pytest.fixture
def session() -> Generator:
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()