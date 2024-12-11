from io import BytesIO
from typing import BinaryIO
from unittest.mock import Mock

import pytest

from invoice_reader import settings
from invoice_reader.core import storage
from invoice_reader.models import S3
from invoice_reader.schemas import FileData

FILEPATH = settings.REPO_DIR / "tests/units/assets/paper.pdf"


class TestS3Storage:
    @pytest.fixture
    def file_data(self):
        return FileData(
            user_id=settings._USER_ID, file=BytesIO(b"file"), filename="filenmame.pdf"
        )

    @pytest.fixture
    def bucket(self):
        return "bucket"

    @pytest.fixture
    def file(self):
        return BytesIO(b"Files")

    @pytest.fixture
    def s3_mocker(self, mocker):
        mock_client = Mock()
        mocker.patch("boto3.client", return_value=mock_client)
        return mock_client

    def test_store_file(
        self, file: BinaryIO, bucket: str, file_data: FileData, s3_mocker: Mock
    ):
        s3_model = S3.init(bucket=bucket, file_data=file_data)
        storage.store_file(file=file, s3_model=s3_model)
        s3_mocker.upload_fileobj.assert_called_with(file, bucket, s3_model.suffix)

    def test_s3_init(self, bucket: str, file_data: FileData):
        s3_model = S3.init(bucket=bucket, file_data=file_data)
        assert (
            s3_model.suffix == f"user-{settings._USER_ID}/file-{file_data.file_id}.pdf"
        )

    def test_no_file_format(self, file: BinaryIO):
        with pytest.raises(ValueError):
            FileData(
                user_id=settings._USER_ID,
                file=file,
                filename="filename",  # missing file format
            )
