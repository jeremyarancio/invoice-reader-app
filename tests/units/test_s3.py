from typing import BinaryIO
from unittest.mock import Mock

import pytest

from invoice_reader.core import storage
from invoice_reader.models import S3, UserModel
from invoice_reader.schemas import FileData


def test_store_file(file: BinaryIO, bucket: str, file_data: FileData, s3_mocker: Mock):
    s3_model = S3.init(bucket=bucket, file_data=file_data)
    storage.store_file(file=file, s3_model=s3_model)
    s3_mocker.upload_fileobj.assert_called_with(file, bucket, s3_model.suffix)


def test_s3_init(bucket: str, file_data: FileData, test_existing_user: UserModel):
    s3_model = S3.init(bucket=bucket, file_data=file_data)
    assert (
        s3_model.suffix
        == f"user-{test_existing_user.user_id}/file-{file_data.file_id}.pdf"
    )


def test_no_file_format(
    file: BinaryIO,
    test_existing_user: UserModel,
):
    with pytest.raises(ValueError):
        FileData(
            user_id=test_existing_user.user_id,
            file=file,
            filename="filename",  # missing file format
        )
