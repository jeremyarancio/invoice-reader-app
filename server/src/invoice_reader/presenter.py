import uuid
from typing import BinaryIO

import sqlmodel
from fastapi import HTTPException

from invoice_reader import settings
from invoice_reader.app.exceptions import (
    CLIENT_NOT_FOUND,
    EXISTING_CLIENT_EXCEPTION,
    EXISTING_INVOICE_EXCEPTION,
    INVOICE_NOT_FOUND,
    MISSING_ENVIRONMENT_VARIABLE_EXCEPTION,
    ROLLBACK,
    UNPROCESSABLE_FILE,
)
from invoice_reader.core import storage
from invoice_reader.infrastructure.parser import parse_invoice
from invoice_reader.infrastructure.storage import S3
from invoice_reader.mappers import (
    ClientMapper,
    CurrencyMapper,
    InvoiceMapper,
    UserMapper,
)
from invoice_reader.repository import (
    ClientRepository,
    CurrencyRepository,
    InvoiceRepository,
    UserRepository,
)
from invoice_reader.schemas import FileData
from invoice_reader.schemas.clients import (
    ClientCreate,
    ClientResponse,
    ClientUpdate,
    PagedClientResponse,
)
from invoice_reader.schemas.invoices import (
    InvoiceCreate,
    InvoiceResponse,
    InvoiceUpdate,
    PagedInvoiceResponse,
)
from invoice_reader.schemas.parser import InvoiceExtraction
from invoice_reader.schemas.users import (
    User,
    UserResponse,
)
from invoice_reader.utils import logger, s3_utils

LOGGER = logger.get_logger(__name__)




def get_user_by_email(email: str, session: sqlmodel.Session) -> User | None:
    user_repository = UserRepository(session=session)
    user_model = user_repository.get_user_by_email(email=email)
    return UserMapper.map_user_model_to_user(user_model) if user_model else None


def add_user(user: User, session: sqlmodel.Session) -> None:
    user_repository = UserRepository(session=session)
    user_model = UserMapper.map_user_to_model(user=user)
    user_repository.add(user_model=user_model)


def get_invoice(
    user_id: uuid.UUID, file_id: uuid.UUID, session: sqlmodel.Session
) -> InvoiceResponse:
    invoice_repository = InvoiceRepository(session=session)
    invoice_model = invoice_repository.get(user_id=user_id, file_id=file_id)
    if invoice_model:
        invoice = InvoiceMapper.map_invoice_model_to_invoice(
            invoice_model=invoice_model
        )
        return InvoiceMapper.map_invoice_to_response(invoice=invoice)
    raise INVOICE_NOT_FOUND


def get_paged_invoices(
    user_id: uuid.UUID, session: sqlmodel.Session, page: int, per_page: int
) -> PagedInvoiceResponse:
    invoice_repository = InvoiceRepository(session=session)
    invoice_models = invoice_repository.get_all(user_id=user_id)
    start = (page - 1) * per_page
    end = start + per_page
    invoices = InvoiceMapper.map_invoice_models_to_invoices(
        invoice_models=invoice_models
    )
    return PagedInvoiceResponse(
        page=page,
        per_page=per_page,
        total=len(invoice_models),
        data=InvoiceMapper.map_invoices_to_responses(invoices=invoices[start:end]),
    )


def add_client(
    user_id: uuid.UUID,
    session: sqlmodel.Session,
    client_create: ClientCreate,
) -> None:
    client_repository = ClientRepository(session=session)
    existing_client = client_repository.get_by_name(
        user_id=user_id, client_name=client_create.client_name
    )
    if existing_client:
        raise EXISTING_CLIENT_EXCEPTION
    client = ClientMapper.map_client_create_to_client(client_create=client_create)
    client_model = ClientMapper.map_client_to_model(client=client, user_id=user_id)
    client_repository.add(client_model=client_model)


def get_client(
    user_id: uuid.UUID, session: sqlmodel.Session, client_id: uuid.UUID
) -> ClientResponse:
    client_repository = ClientRepository(session=session)
    client_model = client_repository.get(user_id=user_id, client_id=client_id)
    if not client_model:
        raise CLIENT_NOT_FOUND
    client = ClientMapper.map_client_model_to_client(client_model=client_model)
    client_response = ClientMapper.map_client_to_response(client=client)
    return client_response


def get_paged_clients(
    user_id: uuid.UUID,
    session: sqlmodel.Session,
    page: int,
    per_page: int,
) -> PagedClientResponse:
    client_repository = ClientRepository(session=session)
    client_models = client_repository.get_all(user_id=user_id, limit=per_page)
    clients = ClientMapper.map_client_models_to_clients(client_models=client_models)
    client_responses = ClientMapper.map_clients_to_responses(clients=clients)
    return PagedClientResponse(
        page=page, per_page=per_page, total=len(clients), data=client_responses
    )


def delete_invoice(
    file_id: uuid.UUID, user_id: uuid.UUID, session: sqlmodel.Session
) -> None:
    if not settings.S3_BUCKET_NAME:
        raise MISSING_ENVIRONMENT_VARIABLE_EXCEPTION
    invoice_repository = InvoiceRepository(session=session)
    invoice_model = invoice_repository.get(file_id=file_id, user_id=user_id)
    if not invoice_model:
        raise INVOICE_NOT_FOUND
    invoice = InvoiceMapper.map_invoice_model_to_invoice(invoice_model=invoice_model)
    invoice_repository.delete(file_id=file_id, user_id=user_id)

    # TODO: implement UOW and rollback
    if not invoice.s3_path:
        raise ROLLBACK
    s3 = S3.init(bucket=settings.S3_BUCKET_NAME)
    suffix = s3_utils.get_suffix_from_s3_path(s3_path=invoice.s3_path)
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
    user_id: uuid.UUID,
    invoice_id: uuid.UUID,
    invoice_update: InvoiceUpdate,
    session: sqlmodel.Session,
) -> None:
    invoice_repository = InvoiceRepository(session=session)
    existing_invoices = invoice_repository.get_all(
        user_id=user_id,
    )
    if not existing_invoices:
        raise HTTPException(
            status_code=500,
            detail=f"Issue with updating invoice: no existing invoices found. Invoice to update: {invoice_update}",
        )
    # Check for duplicate invoice numbers (excluding the current invoice)
    if any(
        invoice.invoice_number == invoice_update.invoice_number
        and invoice.file_id != invoice_id
        for invoice in existing_invoices
    ):
        raise EXISTING_INVOICE_EXCEPTION  # There are multiple invoices with the same number: conflict
    invoice_repository.update(
        invoice_id=invoice_id,
        values_to_update=InvoiceMapper.map_invoice_update_for_model(
            invoice_update=invoice_update
        ),
    )


def get_invoice_url(
    invoice_id: uuid.UUID, user_id: uuid.UUID, session: sqlmodel.Session
) -> str:
    if not settings.S3_BUCKET_NAME:
        raise MISSING_ENVIRONMENT_VARIABLE_EXCEPTION
    s3 = S3.init(bucket=settings.S3_BUCKET_NAME)
    invoice_repository = InvoiceRepository(session=session)
    invoice_model = invoice_repository.get(file_id=invoice_id, user_id=user_id)
    if not invoice_model:
        raise INVOICE_NOT_FOUND
    invoice = InvoiceMapper.map_invoice_model_to_invoice(invoice_model=invoice_model)
    if not invoice.s3_path:
        raise ValueError(f"s3_path of invoice {invoice_id} not found.")
    suffix = s3_utils.get_suffix_from_s3_path(s3_path=invoice.s3_path)
    url = s3.create_presigned_url(suffix=suffix)
    return url


def get_currencies(session: sqlmodel.Session):
    currency_repository = CurrencyRepository(session=session)
    currency_models = currency_repository.get_all()
    currencies = CurrencyMapper.map_currency_models_to_currencies(currency_models)
    return currencies


def update_client(
    user_id: uuid.UUID,
    client_id: uuid.UUID,
    session: sqlmodel.Session,
    client_update: ClientUpdate,
) -> None:
    client_repository = ClientRepository(session=session)
    existing_clients = client_repository.get_all(
        user_id=user_id,
    )
    if not existing_clients:
        raise HTTPException(
            status_code=500,
            detail=f"Issue with updating client: no existing clients found. Client to update: {client_update}",
        )
    # Check for duplicate client names (excluding the current client)
    if any(
        client.client_name == client_update.client_name
        and client.client_id != client_id
        for client in existing_clients
    ):
        raise EXISTING_CLIENT_EXCEPTION  # There are multiple clients with the same name: conflict
    client_repository.update(
        client_id=client_id,
        values_to_update=ClientMapper.map_client_update_for_model(
            client_update=client_update
        ),
    )


def get_user(user_id: uuid.UUID, session: sqlmodel.Session) -> UserResponse:
    user_repository = UserRepository(session=session)
    user_model = user_repository.get(user_id=user_id)
    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")
    return UserMapper.map_user_to_response(
        user=UserMapper.map_user_model_to_user(user_model=user_model)
    )


def extract_invoice(
    file: BinaryIO,
) -> InvoiceExtraction:
    return parse_invoice(file)
