from typing import BinaryIO
import uuid

from invoice_reader.schemas import InvoiceMetadata
from invoice_reader.models import S3
from invoice_reader.settings import S3_BUCKET
from invoice_reader.utils.logger import get_logger


LOGGER = get_logger()


def store(
    user_id: str, file: BinaryIO, metadata: InvoiceMetadata, bucket: str = S3_BUCKET
) -> None:
    try:
        store_file(user_id, file, bucket)
        store_metadata(user_id=user_id, metadata=metadata)
    except Exception as e:
        LOGGER.error(e)
        #TODO: Rollback


def store_file(user_id, file, bucket) -> None:
    file_id = uuid.uuid1()
    s3_file = S3.init_from_id(bucket=bucket, user_id=user_id, file_id=file_id)
    s3_file.store()


def store_metadata(user_id: str, metadata: InvoiceMetadata):
    raise NotImplementedError
