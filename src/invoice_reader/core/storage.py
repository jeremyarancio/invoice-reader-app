from typing import BinaryIO

from invoice_reader.schemas import InvoiceMetadata
from invoice_reader.models import S3
from invoice_reader.utils.logger import get_logger
from invoice_reader.schemas import FileData 

LOGGER = get_logger()


def store(
    file: BinaryIO,
    file_data: FileData,
    metadata: InvoiceMetadata,
    bucket: str | None,
) -> None:
    if not bucket:
        raise ValueError("S3 bucket name was not found as environment variable.")
    try:
        s3_model = S3.init(
            bucket=bucket,
            file_data=file_data
        )
        store_file(file=file, s3_model=s3_model)
        store_metadata(user_id=file_data.user_id, metadata=metadata)
    except Exception as e:
        LOGGER.error(e)
        # TODO: Rollback


def store_file(file: BinaryIO, s3_model: S3) -> None:
    s3_model.store(file=file)
    LOGGER.info("File stored succesfully at %s", s3_model.path)


def store_metadata(user_id: str, metadata: InvoiceMetadata):
    raise NotImplementedError
