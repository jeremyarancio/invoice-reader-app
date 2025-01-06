import uuid
from typing import BinaryIO

import sqlmodel

from invoice_reader import settings
from invoice_reader.app.exceptions import EXISTING_CLIENT_EXCEPTION
from invoice_reader.core import storage
from invoice_reader.models import S3
from invoice_reader.repository import (
    ClientRepository,
    InvoiceRepository,
    UserRepository,
)
from invoice_reader.schemas import (
    Client,
    FileData,
    Invoice,
    InvoiceCreate,
    InvoiceGetResponse,
    PagedClientGetResponse,
    PagedInvoiceGetResponse,
    User,
)
from invoice_reader.utils import logger, s3_utils

LOGGER = logger.get_logger()


def submit(
    user_id: uuid.UUID,
    file: BinaryIO,
    filename: str,
    invoice_data: InvoiceCreate,
    session: sqlmodel.Session,
) -> None:
    file_data = FileData(user_id=user_id, filename=filename)
    s3_model = S3.init(bucket=settings.S3_BUCKET)
    invoice_repository = InvoiceRepository(session=session)
    storage.store(
        file=file,
        file_data=file_data,
        invoice_data=invoice_data,
        invoice_repository=invoice_repository,
        s3_model=s3_model,
    )


def register_user(user: User, session: sqlmodel.Session) -> None:
    user_repository = UserRepository(session=session)
    user_repository.add(user)
    

def get_user_by_email(email: str, session: sqlmodel.Session) -> User | None:
    user_repository = UserRepository(session=session)
    user = user_repository.get_user_by_email(email=email)
    return user


def add_user(user: User, session: sqlmodel.Session) -> None:
    user_repository = UserRepository(session=session)
    user = user_repository.add(user=user)


def get_invoice(
    user: User, file_id: uuid.UUID, session: sqlmodel.Session
) -> InvoiceGetResponse:
    invoice_repository = InvoiceRepository(session=session)
    invoice_response = invoice_repository.get(user_id=user.user_id, file_id=file_id)
    return invoice_response


def get_paged_invoices(
    user: User, session: sqlmodel.Session, page: int, per_page: int
) -> PagedInvoiceGetResponse:
    invoice_repository = InvoiceRepository(session=session)
    invoice_responses = invoice_repository.get_all(user_id=user.user_id)
    start = (page - 1) * per_page
    end = start + per_page
    return PagedInvoiceGetResponse(
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


def get_paged_clients(
    user: User,
    session: sqlmodel.Session,
    page: int,
    per_page: int,
) -> PagedClientGetResponse:
    client_repository = ClientRepository(session=session)
    clients = client_repository.get_all(user_id=user.user_id, limit=per_page)
    return PagedClientGetResponse(
        page=page, per_page=per_page, total=len(clients), data=clients
    )


def delete_invoice(
    file_id: uuid.UUID, user_id: uuid.UUID, session: sqlmodel.Session
) -> None:
    invoice_repository = InvoiceRepository(session=session)
    invoice = invoice_repository.get(file_id=file_id, user_id=user_id)

    invoice_repository.delete(file_id=file_id, user_id=user_id)
    s3 = S3.init(bucket=settings.S3_BUCKET)
    suffix = s3_utils.get_suffix_from_s3_path(invoice.s3_path)
    s3.delete(suffix=suffix)


def delete_client(
    client_id: uuid.UUID, user_id: uuid.UUID, session: sqlmodel.Session
) -> None:
    client_repository = ClientRepository(session=session)
    client_repository.delete(client_id=client_id, user_id=user_id)


def delete_user(user_id: uuid.UUID, session: sqlmodel.Session) -> None:
    user_repository = UserRepository(session=session)
    user_repository.delete(user_id=user_id)


def update_invoice(
    invoice_id: uuid.UUID, invoice: Invoice, session: sqlmodel.Session
) -> None:
    invoice_repository = InvoiceRepository(session=session)
    invoice_repository.update(invoice_id=invoice_id, invoice=invoice)
