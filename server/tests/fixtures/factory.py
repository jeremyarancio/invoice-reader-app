"""Function to fill the test database with elements."""

import uuid

import pytest
from sqlmodel import Session, SQLModel, StaticPool, create_engine

from invoice_reader.app import auth
from invoice_reader.models import (
    ClientModel,
    CurrencyModel,
    InvoiceModel,
    UserModel,
)
from invoice_reader.repository import (
    ClientRepository,
    InvoiceRepository,
    UserRepository,
)
from invoice_reader.schemas import FileData
from invoice_reader.schemas.clients import Client
from invoice_reader.schemas.invoices import Invoice, InvoiceBase
from invoice_reader.schemas.users import User, UserCreate


def add_and_commit(session: Session, *models: SQLModel) -> None:
    for model in models:
        session.add(model)
    session.commit()
    for model in models:
        session.refresh(model)




@pytest.fixture
def existing_user_model(
    existing_user: User, existing_user_create: UserCreate
) -> UserModel:
    return UserModel(
        user_id=existing_user.user_id,
        email=existing_user.email,
        hashed_password=auth.get_password_hash(existing_user_create.password),
        is_disabled=False,
    )


@pytest.fixture
def existing_invoice_model(
    test_existing_user: UserModel,
    test_existing_client: ClientModel,
    s3_suffix: str,
    existing_invoice: InvoiceBase,
    file_data: FileData,
    test_existing_currency: CurrencyModel,
) -> InvoiceModel:
    return InvoiceModel(
        file_id=file_data.file_id,
        s3_path=s3_suffix,
        user_id=test_existing_user.user_id,
        client_id=test_existing_client.client_id,
        currency_id=test_existing_currency.id,
        amount_excluding_tax=existing_invoice.gross_amount,
        invoice_number=existing_invoice.invoice_number,
        invoiced_date=existing_invoice.invoiced_date,
        description=existing_invoice.description,
        vat=existing_invoice.vat,
    )


@pytest.fixture
def existing_invoice_models(
    test_existing_user: UserModel,
    test_existing_client: ClientModel,
    test_existing_currency: CurrencyModel,
    s3_suffix: str,
    existing_invoices: list[Invoice],
) -> list[InvoiceModel]:
    return [
        InvoiceModel(
            file_id=uuid.uuid4(),
            s3_path=s3_suffix,
            user_id=test_existing_user.user_id,
            client_id=test_existing_client.client_id,
            currency_id=test_existing_currency.id,
            amount_excluding_tax=invoice.gross_amount,
            invoice_number=invoice.invoice_number,
            invoiced_date=invoice.invoiced_date,
            description=invoice.description,
            vat=invoice.vat,
            paid_date=invoice.paid_date,
        )
        for invoice in existing_invoices
    ]


@pytest.fixture
def existing_client_model(
    test_existing_user: User,
    existing_client: Client,
) -> ClientModel:
    return ClientModel(
        user_id=test_existing_user.user_id,
        **existing_client.model_dump(),
    )


@pytest.fixture
def existing_client_models(
    test_existing_user: User,
    existing_clients: list[Client],
) -> list[ClientModel]:
    return [
        ClientModel(
            user_id=test_existing_user.user_id,
            **client.model_dump(),
        )
        for client in existing_clients
    ]


@pytest.fixture
def test_existing_user(session: Session, existing_user_model: UserModel) -> UserModel:  # type: ignore
    add_and_commit(session, existing_user_model)
    yield existing_user_model


@pytest.fixture
def test_existing_invoices(
    session: Session,
    existing_invoice_models: list[InvoiceModel],
) -> list[InvoiceModel]:  # type: ignore
    add_and_commit(session, *existing_invoice_models)
    yield existing_invoice_models


@pytest.fixture
def test_existing_invoice(
    session: Session,
    existing_invoice_model: InvoiceModel,
) -> InvoiceModel:  # type: ignore
    add_and_commit(session, existing_invoice_model)
    yield existing_invoice_model


@pytest.fixture
def test_existing_clients(
    session: Session, existing_client_models: list[ClientModel]
) -> list[ClientModel]:  # type: ignore
    add_and_commit(session, *existing_client_models)
    yield existing_client_models


@pytest.fixture
def test_existing_client(
    session: Session,
    existing_client_model: ClientModel,
) -> ClientModel:  # type: ignore
    add_and_commit(session, existing_client_model)
    yield existing_client_model


@pytest.fixture
def test_existing_currency(
    session: Session, existing_currency: CurrencyModel
) -> CurrencyModel:
    add_and_commit(session, existing_currency)
    yield existing_currency


@pytest.fixture
def invoice_repository(session: Session) -> InvoiceRepository:
    return InvoiceRepository(session=session)


@pytest.fixture
def client_repository(session: Session) -> ClientRepository:
    return ClientRepository(session=session)


@pytest.fixture
def user_repository(session: Session) -> UserRepository:
    return UserRepository(session=session)
