import os
from typing import BinaryIO

from invoice_reader.core import storage
from invoice_reader.schemas import InvoiceMetadata
from invoice_reader import settings


def submit(user_id: str, file: BinaryIO, filename: str, metadata: InvoiceMetadata):
    file_format = os.path.splitext(filename)[-1]
    storage.store(
        user_id=user_id,
        file=file,
        file_format=file_format,
        metadata=metadata,
        bucket=settings.S3_BUCKET,
    )


def extract(file: BinaryIO) -> InvoiceMetadata:
    raise NotImplementedError


def get_user_id(token: str):
    raise NotImplementedError
