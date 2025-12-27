from typing import Annotated

import sqlmodel
from fastapi import Depends
from sqlalchemy.engine import Engine
from sqlalchemy.pool import QueuePool

from invoice_reader.infrastructure.models import *  # noqa: F403
from invoice_reader.infrastructure.repositories import (
    S3FileRepository,
    SQLModelClientRepository,
    SQLModelInvoiceRepository,
    SQLModelUserRepository,
)
from invoice_reader.infrastructure.repositories.exchange_rate import InMemoryExchangeRateRepository
from invoice_reader.services.interfaces.repositories import (
    IClientRepository,
    IFileRepository,
    IInvoiceRepository,
    IUserRepository,
)
from invoice_reader.services.interfaces.repositories.exchange_rate import IExchangeRateRepository
from invoice_reader.settings import get_settings

settings = get_settings()


def get_engine() -> Engine:
    """
    Create database engine with connection pooling.
    Uses lru_cache to create a singleton engine shared across all requests.
    """
    return sqlmodel.create_engine(
        settings.database_url,
        echo=False,
        # Connection pooling configuration
        poolclass=QueuePool,
        pool_size=10,  # Maintain 10 connections per worker
        max_overflow=20,  # Allow up to 20 additional connections under load
        pool_pre_ping=True,  # Verify connections are alive before using
        pool_recycle=3600,  # Recycle connections after 1 hour (3600 seconds)
    )


def get_session(engine: Annotated[Engine, Depends(get_engine)]):
    with sqlmodel.Session(engine) as session:
        yield session


def get_file_repository() -> IFileRepository:
    return S3FileRepository(
        bucket=settings.s3_bucket_name,
        region=settings.s3_region,
        presigned_url_expiration=settings.presigned_url_expiration,
    )


def get_invoice_repository(
    session: Annotated[sqlmodel.Session, Depends(get_session)],
) -> IInvoiceRepository:
    return SQLModelInvoiceRepository(session=session)


def get_client_repository(
    session: Annotated[sqlmodel.Session, Depends(get_session)],
) -> IClientRepository:
    return SQLModelClientRepository(session=session)


def get_user_repository(
    session: Annotated[sqlmodel.Session, Depends(get_session)],
) -> IUserRepository:
    return SQLModelUserRepository(session=session)


def get_exchange_rate_repository() -> IExchangeRateRepository:
    return InMemoryExchangeRateRepository()
