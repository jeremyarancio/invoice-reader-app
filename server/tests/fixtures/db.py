from collections.abc import Generator

import pytest
from sqlalchemy import StaticPool
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

from invoice_reader.infrastructure.models import *  # noqa: F401, F403


@pytest.fixture(scope="function")
def engine() -> Engine:
    return create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )


@pytest.fixture
def session(engine: Engine) -> Generator[Session, None, None]:
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
