import uuid
from typing import BinaryIO

import sqlmodel

from invoice_reader.app.exceptions import EXISTING_CLIENT_EXCEPTION
from invoice_reader import settings
from invoice_reader.core import storage
from invoice_reader.models import S3
from invoice_reader.repository import (
    InvoiceRepository,
    UserRepository,
    ClientRepository,
)
from invoice_reader.schemas import (
    FileData,
    InvoiceCreate,
    InvoiceResponse,
    PagedInvoiceResponse,
    User,
    Client,
)
from invoice_reader.utils import logger


LOGGER = logger.get_logger()


def submit(
    user_id: uuid.UUID,
    file: BinaryIO,
    filename: str,
    invoice_data: InvoiceCreate,
    session: sqlmodel.Session,
):
    file_data = FileData(user_id=user_id, filename=filename)
    s3_model = S3.init(bucket=settings.S3_BUCKET, file_data=file_data)
    invoice_repository = InvoiceRepository(session=session)
    storage.store(
        file=file,
        file_data=file_data,
        invoice_data=invoice_data,
        s3_model=s3_model,
        invoice_repository=invoice_repository,
    )


def get_user(token: str):
    raise NotImplementedError


def register_user(user: User, session: sqlmodel.Session) -> None:
    user_repository = UserRepository(session=session)
    user_repository.add(user)


def get_user_by_username(username: str, session: sqlmodel.Session) -> User:
    user_repository = UserRepository(session=session)
    user = user_repository.get_by_username(username)
    return user


def get_user_by_email(email: str, session: sqlmodel.Session) -> User | None:
    user_repository = UserRepository(session=session)
    user = user_repository.get_user_by_email(email=email)
    return user


def add_user(user: User, session: sqlmodel.Session) -> None:
    user_repository = UserRepository(session=session)
    user = user_repository.add(user=user)


def get_invoice(
    user: User, file_id: uuid.UUID, session: sqlmodel.Session
) -> InvoiceResponse:
    invoice_repository = InvoiceRepository(session=session)
    invoice_response = invoice_repository.get(user_id=user.user_id, file_id=file_id)
    return invoice_response


def get_paged_invoices(
    user: User, session: sqlmodel.Session, page: int, per_page: int
) -> PagedInvoiceResponse:
    invoice_repository = InvoiceRepository(session=session)
    invoice_responses = invoice_repository.get_all(user_id=user.user_id)
    start = (page - 1) * per_page
    end = start + per_page
    return PagedInvoiceResponse(
        page=page,
        per_page=per_page,
        total=len(invoice_responses),
        data=invoice_responses[start:end],
    )


def add_client(user: User, session: sqlmodel.Session, client: Client) -> None:
    client_repository = ClientRepository(session=session)
    existing_client = client_repository.get_by_name(
        user_id=user.user_id, client_name=client.client_name
    )
    if existing_client:
        raise EXISTING_CLIENT_EXCEPTION
    client_repository.add(user_id=user.user_id, client=client)
    LOGGER.info("New client added to the database.")