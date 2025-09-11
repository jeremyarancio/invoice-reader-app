from typing import Generator

import pytest
from sqlalchemy import StaticPool
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.engine import Engine

from invoice_reader.infrastructure.models import *


@pytest.fixture(scope="session")
def engine() -> Engine:
    return create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )


@pytest.fixture
def session_fixture(engine: Engine) -> Generator[Session, None, None]:
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
