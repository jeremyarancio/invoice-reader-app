import uuid
from typing import BinaryIO

import sqlmodel

from invoice_reader import settings
from invoice_reader.app.exceptions import (
    CLIENT_NOT_FOUND,
    EXISTING_CLIENT_EXCEPTION,
    MISSING_ENVIRONMENT_VARIABLE_EXCEPTION,
    UNPROCESSABLE_FILE,
)
from invoice_reader.core import storage
from invoice_reader.mappers.clients import ClientMapper
from invoice_reader.models import S3
from invoice_reader.repository import (
    ClientRepository,
    InvoiceRepository,
    UserRepository,
)
from invoice_reader.schemas import FileData, client_schema, invoice_schema, user_schema
from invoice_reader.utils import logger, s3_utils

LOGGER = logger.get_logger()


def submit_invoice(
    user_id: uuid.UUID,
    file: BinaryIO,
    filename: str | None,
    invoice_data: invoice_schema.InvoiceCreate,
    session: sqlmodel.Session,
) -> None:
    if not filename:
        raise UNPROCESSABLE_FILE
    if not settings.S3_BUCKET_NAME:
        raise MISSING_ENVIRONMENT_VARIABLE_EXCEPTION
    file_data = FileData(user_id=user_id, filename=filename)
    s3_model = S3.init(bucket=settings.S3_BUCKET_NAME)
    invoice_repository = InvoiceRepository(session=session)
    storage.store(
        file=file,
        file_data=file_data,
        invoice_data=invoice_data,
        invoice_repository=invoice_repository,
        s3_model=s3_model,
    )


def register_user(user: user_schema.User, session: sqlmodel.Session) -> None:
    user_repository = UserRepository(session=session)
    user_repository.add(user)


def get_user_by_email(email: str, session: sqlmodel.Session) -> user_schema.User | None:
    user_repository = UserRepository(session=session)
    user = user_repository.get_user_by_email(email=email)
    return user


def add_user(user: user_schema.User, session: sqlmodel.Session) -> None:
    user_repository = UserRepository(session=session)
    user_repository.add(user=user)


def get_invoice(
    user: user_schema.User, file_id: uuid.UUID, session: sqlmodel.Session
) -> invoice_schema.InvoiceGetResponse:
    invoice_repository = InvoiceRepository(session=session)
    invoice_response = invoice_repository.get(user_id=user.user_id, file_id=file_id)
    return invoice_response


def get_paged_invoices(
    user: user_schema.User, session: sqlmodel.Session, page: int, per_page: int
) -> invoice_schema.PagedInvoiceGetResponse:
    invoice_repository = InvoiceRepository(session=session)
    invoice_responses = invoice_repository.get_all(user_id=user.user_id)
    start = (page - 1) * per_page
    end = start + per_page
    return invoice_schema.PagedInvoiceGetResponse(
        page=page,
        per_page=per_page,
        total=len(invoice_responses),
        data=invoice_responses[start:end],
    )


def add_client(
    user: user_schema.User, session: sqlmodel.Session, client: client_schema.Client
) -> None:
    client_repository = ClientRepository(session=session)
    existing_client = client_repository.get_by_name(
        user_id=user.user_id, client_name=client.client_name
    )
    if existing_client:
        raise EXISTING_CLIENT_EXCEPTION
    client_repository.add(user_id=user.user_id, client=client)
    LOGGER.info("New client added to the database.")


def get_client(
    user: user_schema.User, session: sqlmodel.Session, client_id: uuid.UUID
) -> client_schema.ClientResponse:
    client_repository = ClientRepository(session=session)
    client_model = client_repository.get(user_id=user.user_id, client_id=client_id)
    if not client_model:
        raise CLIENT_NOT_FOUND
    client = ClientMapper.map_client_model_to_client(client_model=client_model)
    client_response = ClientMapper.map_client_to_response(client)
    return client_response


def get_paged_clients(
    user: user_schema.User,
    session: sqlmodel.Session,
    page: int,
    per_page: int,
) -> client_schema.PagedClientResponse:
    client_repository = ClientRepository(session=session)
    clients = ClientMapper.map_client_models_to_clients(
        client_repository.get_all(user_id=user.user_id, limit=per_page)
    )
    client_responses = ClientMapper.map_clients_to_responses(clients=clients)
    return client_schema.PagedClientResponse(
        page=page, per_page=per_page, total=len(clients), data=client_responses
    )


def delete_invoice(
    file_id: uuid.UUID, user_id: uuid.UUID, session: sqlmodel.Session
) -> None:
    if not settings.S3_BUCKET_NAME:
        raise MISSING_ENVIRONMENT_VARIABLE_EXCEPTION
    invoice_repository = InvoiceRepository(session=session)
    invoice = invoice_repository.get(file_id=file_id, user_id=user_id)
    invoice_repository.delete(file_id=file_id, user_id=user_id)
    s3 = S3.init(bucket=settings.S3_BUCKET_NAME)
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
    invoice_id: uuid.UUID, invoice: invoice_schema.Invoice, session: sqlmodel.Session
) -> None:
    invoice_repository = InvoiceRepository(session=session)
    invoice_repository.update(invoice_id=invoice_id, invoice=invoice)


def get_invoice_url(
    invoice_id: uuid.UUID, user_id: uuid.UUID, session: sqlmodel.Session
) -> str:
    if not settings.S3_BUCKET_NAME:
        raise MISSING_ENVIRONMENT_VARIABLE_EXCEPTION
    s3 = S3.init(bucket=settings.S3_BUCKET_NAME)
    invoice_repository = InvoiceRepository(session=session)
    invoice = invoice_repository.get(
        file_id=invoice_id, user_id=user_id
    )  # TODO: horrible! Refactor this s*** with proper mappers & schemas
    suffix = s3_utils.get_suffix_from_s3_path(s3_path=invoice.s3_path)
    url = s3.create_presigned_url(suffix=suffix)
    return url
