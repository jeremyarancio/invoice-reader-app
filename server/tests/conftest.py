# from io import BytesIO
from ast import In
from pathlib import Path
# from unittest.mock import Mock

import pytest

from invoice_reader.infrastructure.repositories.invoice import InMemoryInvoiceRepository
from invoice_reader.infrastructure.repositories.file import InMemoryFileRepository
from invoice_reader.infrastructure.repositories.client import InMemoryClientRepository
from invoice_reader.infrastructure.repositories.user import InMemoryUserRepository

pytest_plugins = [
    "tests.fixtures.db",
    "tests.fixtures.domain.client",
    "tests.fixtures.domain.invoice",
    "tests.fixtures.domain.user",
]

InMemoryInvoiceRepository.init()

# @pytest.fixture()
# def api_client(session: Session):
#     def get_session_override():
#         return session

#     app.dependency_overrides[db.get_session] = get_session_override
#     client = TestClient(app)
#     yield client
#     app.dependency_overrides.clear()


# @pytest.fixture
# def file_data(existing_user: User, filepath: Path) -> FileData:
#     return FileData(user_id=existing_user.user_id, filename=filepath.name)


# @pytest.fixture
# def file():
#     return BytesIO(b"Files")


# @pytest.fixture
# def s3_bucket() -> str:
#     return "bucket"


# @pytest.fixture
# def s3_suffix(file_data: FileData) -> str:
#     return f"{file_data.user_id}/{file_data.file_id}{file_data.file_format}"


# @pytest.fixture
# def s3_path(s3_bucket: str, s3_suffix) -> str:
#     return f"s3://{s3_bucket}/{s3_suffix}"


# @pytest.fixture
# def s3_mocker(mocker) -> Mock:
#     mock_client = Mock()
#     mocker.patch("boto3.client", return_value=mock_client)
#     return mock_client


# @pytest.fixture
# def bucket() -> str:
#     return "bucket"


# @pytest.fixture
# def auth_token(test_existing_user: UserModel) -> AuthToken:
#     access_token = auth.create_token(
#         email=test_existing_user.email, expire=100, token_type="access"
#     )
#     return AuthToken(access_token=access_token, token_type="bearer")


# @pytest.fixture
# def wrong_files(request, filepath: str):
#     """Used in 'test_submit_invoice_with_wrong_format'"""
#     key, mime_type = request.param
#     with open(filepath, "rb") as f:
#         files = {key: (key, f, mime_type)}
#         yield files
