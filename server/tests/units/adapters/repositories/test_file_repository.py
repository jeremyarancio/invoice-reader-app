import io
from unittest.mock import MagicMock, patch

import pytest

from invoice_reader.domain.invoice import File
from invoice_reader.infrastructure.repositories.file import S3FileRepository


@pytest.fixture(scope="session")
def s3_client_mock():
    with patch("boto3.client") as mock_client:
        client_instance = MagicMock()
        mock_client.return_value = client_instance
        yield client_instance


@pytest.fixture
def repository(s3_client_mock: MagicMock) -> S3FileRepository:
    repo = S3FileRepository(bucket="test-bucket", region="us-east-1", presigned_url_expiration=3600)
    repo.client = s3_client_mock
    return repo


@pytest.fixture
def file():
    return File(
        filename="test.pdf",
        file=io.BytesIO(b"dummy data").read(),
        storage_path="s3://test-bucket/test.pdf",
    )


def test_create_storage_path(repository: S3FileRepository):
    path = repository.create_storage_path("folder/test.pdf")
    assert path == "s3://test-bucket/folder/test.pdf"


def test_store_file(
    s3_client_mock: MagicMock,
    repository: S3FileRepository,
    file: File,
):
    repository.store(file)
    assert s3_client_mock.upload_fileobj.called
    call_args = s3_client_mock.upload_fileobj.call_args[0]
    assert call_args[1] == "test-bucket"
    assert call_args[2] == "test.pdf"


def test_delete_file(repository: S3FileRepository, s3_client_mock: MagicMock):
    repository.delete("s3://test-bucket/test.pdf")
    s3_client_mock.delete_object.assert_called_with(Bucket="test-bucket", Key="test.pdf")


def test_get_url(repository: S3FileRepository, s3_client_mock: MagicMock):
    s3_client_mock.generate_presigned_url.return_value = "https://presigned-url"
    url = repository.get_url("s3://test-bucket/test.pdf")
    assert s3_client_mock.generate_presigned_url.called
    assert url == "https://presigned-url"
