from typing import BinaryIO
from unittest.mock import Mock

import pytest

from invoice_reader.core import storage
from invoice_reader.models import S3, UserModel
from invoice_reader.schemas import FileData
from invoice_reader.utils import s3_utils


def test_store_file(file: BinaryIO, bucket: str, s3_suffix: str, s3_mocker: Mock):
    s3_model = S3.init(bucket=bucket)
    storage.store_file(file=file, s3_model=s3_model, s3_suffix=s3_suffix)
    s3_mocker.upload_fileobj.assert_called_with(file, bucket, s3_suffix)


def test_get_s3_suffix_from_data(s3_suffix: str, file_data: FileData):
    test_suffix = s3_utils.get_s3_suffix_from_data(
        user_id=file_data.user_id,
        file_id=file_data.file_id,
        file_format=file_data.file_format,
    )
    assert test_suffix == s3_suffix


def test_no_file_format(
    test_existing_user: UserModel,
):
    with pytest.raises(ValueError):
        FileData(
            user_id=test_existing_user.user_id,
            filename="filename",  # missing file format
        )


def test_get_suffix_from_s3_path(s3_path: str, s3_suffix: str):
    test_suffix = s3_utils.get_suffix_from_s3_path(s3_path=s3_path)
    assert s3_suffix == test_suffix


def test_delete_s3_object(bucket: str, s3_suffix: str, s3_mocker: Mock):
    s3 = S3.init(bucket=bucket)
    s3.delete(suffix=s3_suffix)
    s3_mocker.delete_object.assert_called_once()
