from typing import BinaryIO

from invoice_reader.mappers import InvoiceMapper
from invoice_reader.models import S3
from invoice_reader.repository import InvoiceRepository
from invoice_reader.schemas import FileData, invoice_schema
from invoice_reader.utils import logger, s3_utils

LOGGER = logger.get_logger()


def store(
    file: BinaryIO,
    file_data: FileData,
    invoice: invoice_schema.InvoicePresenter,
    invoice_repository: InvoiceRepository,
    s3_model: S3,
) -> None:
    s3_suffix = s3_utils.get_s3_suffix_from_data(
        user_id=file_data.user_id,
        file_id=file_data.file_id,
        file_format=file_data.file_format,
    )
    invoice.s3_path = s3_utils.get_s3_path(bucket=s3_model.bucket, suffix=s3_suffix)
    invoice.file_id = file_data.file_id
    # Remove file data at the end
    store_invoice_data(
        file_data=file_data,
        invoice_repository=invoice_repository,
        invoice=invoice,
    )
    store_file(file=file, s3_suffix=s3_suffix, s3_model=s3_model)
    # TODO: Rollback


def store_file(file: BinaryIO, s3_suffix: str, s3_model: S3) -> None:
    s3_model.store(file=file, suffix=s3_suffix)
    LOGGER.info("File stored succesfully at %s", s3_suffix)


def store_invoice_data(
    file_data: FileData,
    invoice: invoice_schema.InvoicePresenter,
    invoice_repository: InvoiceRepository,
) -> None:
    invoice_model = InvoiceMapper.map_invoice_to_model(
        invoice=invoice,
        user_id=file_data.user_id,
    )
    invoice_repository.add(
        user_id=file_data.user_id,
        invoice_model=invoice_model,
    )
