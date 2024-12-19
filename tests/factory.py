"""Function to fill the test database with elements."""

import uuid
from datetime import date

import pytest
from sqlmodel import Session, SQLModel, StaticPool, create_engine

from invoice_reader.app import auth
from invoice_reader.models import (
    ClientModel,
    InvoiceModel,
    UserModel,
)
from invoice_reader.schemas import (
    Client,
    Invoice,
    User,
    UserCreate,
)


@pytest.fixture(name="session")
def session_fixture() -> Session:  # type: ignore
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def add_and_commit(session: Session, *models: list[SQLModel]) -> None:
    session.add_all(models)
    session.commit()
    session.refresh(*models)


def delete_and_commit(session: Session, *models: list[SQLModel]) -> None:
    for model in models:
        session.delete(model)
    session.commit()


@pytest.fixture
def user_create():
    return UserCreate(email="jeremy@email.com", password="password")


@pytest.fixture
def user(user_create: UserCreate):
    return User(
        user_id=uuid.uuid4(),
        email=user_create.email,
        hashed_password=auth.get_password_hash(user_create.password),
        is_disabled=False,
    )


@pytest.fixture
def new_invoice():
    return Invoice(
        invoiced_date=date(2024, 11, 18),
        invoice_number="14SQ456",
        amount_excluding_tax=10000,
        currency="€",
        vat="20",
    )


@pytest.fixture
def new_client():
    return Client(
        client_id=uuid.uuid4(),
        client_name="Sacha&Cie",
        street_number="19",
        street_address="road of coal",
        city="Carcassone",
        country="France",
        zipcode=45777,
    )


@pytest.fixture
def user_model(user: User) -> UserModel:
    return UserModel(
        user_id=user.user_id,
        email=user.email,
        hashed_password=auth.get_password_hash(user.hashed_password),
        is_disabled=False,
    )


@pytest.fixture
def invoice_models(
    user_id: uuid.UUID,
    client_id: uuid.UUID,
    s3_suffix: str,
    invoice: Invoice,
) -> list[InvoiceModel]:
    return [
        InvoiceModel(
            file_id=uuid.uuid4(),  # To respect unique primary key we update the id at each iteration
            s3_path=s3_suffix,
            user_id=user_id,
            client_id=client_id,
            **invoice.model_dump(),
        )
    ]


@pytest.fixture
def invoice_model(
    user: User,
    client: Client,
    s3_suffix: str,
    invoice: Invoice,
) -> list[InvoiceModel]:
    return InvoiceModel(
        file_id=uuid.uuid4(),
        s3_path=s3_suffix,
        user_id=user.user_id,
        client_id=client.client_id,
        **invoice.model_dump(),
    )


@pytest.fixture
def client_models(
    user_id: uuid.UUID,
    client: Client,
) -> list[ClientModel]:
    return [ClientModel(client_id=uuid.uuid4(), user_id=user_id, **client.model_dump())]


@pytest.fixture
def test_user(session: Session, user_model: UserModel) -> UserModel:
    add_and_commit(session, user_model)
    return user_model


@pytest.fixture
def test_invoices(
    session: Session,
    invoice_models: list[InvoiceModel],
) -> list[InvoiceModel]:
    add_and_commit(session, invoice_models)
    return invoice_models


@pytest.fixture
def test_invoice(
    session: Session,
    invoice_model: InvoiceModel,
) -> InvoiceModel:
    add_and_commit(session, invoice_model)
    return invoice_model


@pytest.fixture
def test_clients(
    session: Session, client_models: list[ClientModel]
) -> list[ClientModel]:
    add_and_commit(session, client_models)
    return client_models


@pytest.fixture
def test_client(
    session: Session,
    client_model: ClientModel,
) -> ClientModel:
    add_and_commit(session, client_model)
    return client_model
