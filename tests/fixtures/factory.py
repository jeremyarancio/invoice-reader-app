"""Function to fill the test database with elements."""

import uuid

import pytest
from sqlmodel import Session, SQLModel, StaticPool, create_engine

from invoice_reader.app import auth
from invoice_reader.models import (
    ClientModel,
    InvoiceModel,
    UserModel,
)
from invoice_reader.repository import (
    InvoiceRepository,
)
from invoice_reader.schemas import (
    Client,
    FileData,
    Invoice,
    User,
)


def add_and_commit(session: Session, *models: SQLModel) -> None:
    for model in models:
        session.add(model)
    session.commit()
    for model in models:
        session.refresh(model)


@pytest.fixture(name="session", scope="function")
def session_fixture() -> Session:  # type: ignore
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def existing_user_model(existing_user: User) -> UserModel:
    return UserModel(
        user_id=existing_user.user_id,
        email=existing_user.email,
        hashed_password=auth.get_password_hash(existing_user.hashed_password),
        is_disabled=False,
    )


@pytest.fixture
def existing_invoice_model(
    existing_user: User,
    existing_client: Client,
    s3_suffix: str,
    existing_invoice: Invoice,
    file_data: FileData
) -> InvoiceModel:
    return InvoiceModel(
        file_id=file_data.file_id,
        s3_path=s3_suffix,
        user_id=existing_user.user_id,
        client_id=existing_client.client_id,
        **existing_invoice.model_dump(),
    )


@pytest.fixture
def existing_invoice_models(
    existing_user: User,
    existing_client: Client,
    s3_suffix: str,
    existing_invoices: list[Invoice],
) -> list[InvoiceModel]:
    return [
        InvoiceModel(
            file_id=uuid.uuid4(),
            s3_path=s3_suffix,
            user_id=existing_user.user_id,
            client_id=existing_client.client_id,
            **invoice.model_dump(),
        )
        for invoice in existing_invoices
    ]


@pytest.fixture
def existing_client_model(
    existing_user: User,
    existing_client: Client,
) -> ClientModel:
    return ClientModel(
        client_id=uuid.uuid4(),
        user_id=existing_user.user_id,
        **existing_client.model_dump(),
    )


@pytest.fixture
def existing_client_models(
    existing_user: User,
    existing_clients: list[Client],
) -> list[ClientModel]:
    return [
        ClientModel(
            client_id=uuid.uuid4(),
            user_id=existing_user.user_id,
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
def invoice_repository(session: Session) -> InvoiceRepository:
    return InvoiceRepository(session=session)
