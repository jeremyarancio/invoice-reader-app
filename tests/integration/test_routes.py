from unittest.mock import Mock
import datetime

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, StaticPool

from invoice_reader.app.routes import app
from invoice_reader.db import get_session
from invoice_reader import models  # noqa: F401
from invoice_reader.schemas import InvoiceSchema, FileData


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
def files():
    with open("tests/assets/paper.pdf", "rb") as f:
        files = {"upload_file": ("filename", f, "application/pdf")}
        yield files


@pytest.fixture
def file_data() -> FileData:
    return FileData(
        user_id="jeremy1234",
        filename="filename.pdf"
    )


@pytest.fixture
def s3_suffix(file_data: FileData) -> str:
    return f"{file_data.user_id}/{file_data.file_id}{file_data.file_format}"


@pytest.fixture
def s3_mocker(mocker) -> Mock:
    mock_client = Mock()
    mocker.patch("boto3.client", return_value=mock_client)
    return mock_client


@pytest.fixture
def bucket() -> str:
    return "bucket"


@pytest.fixture
def invoice_schema():
    return InvoiceSchema(
        street_number="19",
        street_name="road of coal",
        city="Carcassone",
        country="France",
        zipcode=45777,
        client_name="Sacha&Cie",
        invoiced_date=datetime.date(2024, 11, 18),
        number="14SQ456",
        excluding_tax=10000,
        # currency="€",
        vat="20",
    )


def test_add_invoice(
    files,
    client: TestClient, 
    s3_mocker: Mock,
    invoice_schema: InvoiceSchema,
):
    data = invoice_schema.model_dump()
    data = {k: (str(v) if isinstance(v, datetime.date) else v) for k, v in data.items()}
    response = client.post(
        url="api/v1/add/",
        # headers = {"Content-Type": "multipart/form-data"},
        data=data,
        files=files
    )
    assert response.status_code == 200
    s3_mocker.assert_called_once()
