from unittest.mock import Mock
from io import BytesIO
from typing import BinaryIO
import datetime

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, StaticPool

from invoice_reader.app.routes import app
from invoice_reader.db import get_session
from invoice_reader import models  # noqa: F401
from invoice_reader.schemas import InvoiceSchema, ClientAdresseSchema, RevenuSchema


@pytest.fixture(name="session")  
def session_fixture():  
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session  


@pytest.fixture(name="client")  
def client_fixture(session: Session):

    def get_session_override():  
        return session
    
    app.dependency_overrides[get_session] = get_session_override  
    client = TestClient(app)  
    yield client  
    app.dependency_overrides.clear()


@pytest.fixture
def file():
    return BytesIO(b"Files")


@pytest.fixture
def s3_mocker(mocker):
    mock_client = Mock()
    mocker.patch("boto3.client", return_value=mock_client)
    return mock_client


@pytest.fixture
def invoice_schema():
    return InvoiceSchema(
        client_adresse=ClientAdresseSchema(
            street_number="19",
            street_name="road of coal",
            city="Carcassone",
            country="France",
            zipcode=45777
        ),
        client_name="Sacha&Cie",
        invoiced_date=datetime.date(2024, 11, 18),
        number="14SQ456",
        revenu=RevenuSchema(
            excluding_tax=10000,
            currency="€",
            vat="20",
        ),
    )


def test_add_invoice(
    file: BinaryIO,
    invoice_schema: InvoiceSchema, 
    client: TestClient, 
    s3_mocker: Mock
):
    client.post("api/v1/add", file=file)

