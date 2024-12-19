
from pathlib import Path
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from invoice_reader import db
from invoice_reader.app import auth, routes
from invoice_reader.schemas import (
    AuthToken,
    Client,
    FileData,
    Invoice,
    InvoiceCreate,
    User,
)


@pytest.fixture()
def api_client(session: Session):
    def get_session_override():
        return session

    routes.app.dependency_overrides[db.get_session] = get_session_override
    client = TestClient(routes.app)
    yield client
    routes.app.dependency_overrides.clear()


@pytest.fixture
def filepath() -> Path:
    return Path("tests/assets/paper.pdf")


@pytest.fixture
def upload_files(filepath):
    with open(filepath, "rb") as f:
        files = {"upload_file": ("filename.pdf", f, "application/pdf")}
        yield files


@pytest.fixture
def file_data(user: User, filepath: Path) -> FileData:
    return FileData(user_id=user.user_id, filename=filepath.name)


@pytest.fixture
def s3_bucket() -> str:
    return "bucket"


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
def auth_token(user: User) -> AuthToken:
    access_token = auth.create_access_token(email=user.email)
    return AuthToken(access_token=access_token, token_type="bearer")


@pytest.fixture
def wrong_files(request, filepath: str):
    """Used in 'test_submit_invoice_with_wrong_format'"""
    key, mime_type = request.param
    with open(filepath, "rb") as f:
        files = {key: (key, f, mime_type)}
        yield files


@pytest.fixture
def invoice_create(client: Client, invoice: Invoice) -> InvoiceCreate:
    return InvoiceCreate(client_id=client.client_id, invoice=invoice)
