from typing import BinaryIO
import uuid

from invoice_reader.schemas import InvoiceMetadata
from invoice_reader.models import S3
from invoice_reader.utils.logger import get_logger


LOGGER = get_logger()


def store(
    user_id: str,
    file: BinaryIO,
    file_format: str,
    metadata: InvoiceMetadata,
    bucket: str | None,
) -> None:
    if not bucket:
        raise ValueError("S3 bucket name was not found as environment variable.")
    try:
        file_id = uuid.uuid1()
        s3_model = S3.init_from_id(
            bucket=bucket,
            user_id=user_id,
            file_id=file_id,
            file_format=file_format
        )
        store_file(file=file, s3_model=s3_model)
        store_metadata(user_id=user_id, metadata=metadata)
    except Exception as e:
        LOGGER.error(e)
        # TODO: Rollback


def store_file(file: BinaryIO, s3_model: S3) -> None:
    s3_model.store(file=file)
    LOGGER.info("File stored succesfully at %s", s3_model.path)


def store_metadata(user_id: str, metadata: InvoiceMetadata):
    raise NotImplementedError
