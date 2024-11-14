import os
from typing import BinaryIO
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import Mock

import pytest

from invoice_reader.core import storage
from invoice_reader import settings
from invoice_reader.models import S3


FILEPATH = settings.REPO_DIR / "tests/units/assets/paper.pdf"


@dataclass
class FileStorageData:
    user_id: str
    file: BinaryIO
    file_format: str
    bucket: str

    @classmethod
    def init(cls, user_id: str, filepath: Path, bucket: str):
        file_format = os.path.splitext(filepath.name)[-1]
        with filepath.open(mode="rb") as file:
            return cls(
                user_id=user_id,
                file=file.read(),
                file_format=file_format,
                bucket=bucket
            )


class TestS3Storage:
    @pytest.fixture
    def file_storage_data(self):
        return FileStorageData.init(
            user_id="user_id",
            filepath=FILEPATH,
            bucket="bucket"
        )
    
    @pytest.fixture
    def s3_mocker(self, mocker):
        mock_client = Mock()
        mocker.patch("boto3.client", return_value=mock_client)
        return mock_client

    def test_store_file(self, file_storage_data: FileStorageData, s3_mocker: Mock):
        s3_model = S3.init_from_id(
            bucket=file_storage_data.bucket,
            file_format=file_storage_data.file_format,
            file_id="file-1234",
            user_id=file_storage_data.user_id
        )        
        storage.store_file(
            file=file_storage_data.file,
            s3_model=s3_model
        )   
        s3_mocker.upload_fileobj.assert_called_with(
            file_storage_data.file, 
            file_storage_data.bucket,
            s3_model.suffix
        )
