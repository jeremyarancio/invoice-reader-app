from typing import BinaryIO

from invoice_reader.app.exceptions import ROLLBACK, ExistingInvoiceException
from invoice_reader.infrastructure.repositories.file import S3
from invoice_reader.mappers import InvoiceMapper
from invoice_reader.repository import InvoiceRepository
from invoice_reader.schemas import FileData
from invoice_reader.schemas.invoices import Invoice
from invoice_reader.utils import logger, s3_utils

LOGGER = logger.get_logger(__name__)


def store(
    file: BinaryIO,
    file_data: FileData,
    invoice: Invoice,
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

    try:
        store_invoice_data(
            file_data=file_data,
            invoice_repository=invoice_repository,
            invoice=invoice,
        )
        store_file(file=file, s3_suffix=s3_suffix, s3_model=s3_model)
    except ExistingInvoiceException:
        raise
    except Exception as e:
        LOGGER.error(
            "Something happened during the invoice submission process: %s. Start rollback.",
            e,
        )
        rollback(
            s3_model=s3_model,
            s3_suffix=s3_suffix,
            file_data=file_data,
            invoice_repository=invoice_repository,
        )


def store_file(file: BinaryIO, s3_suffix: str, s3_model: S3) -> None:
    s3_model.store(file=file, suffix=s3_suffix)
    LOGGER.info("File stored succesfully at %s", s3_suffix)


def store_invoice_data(
    file_data: FileData,
    invoice: Invoice,
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


def rollback(
    s3_model: S3,
    s3_suffix: str,
    file_data: FileData,
    invoice_repository: InvoiceRepository,
) -> None:
    """Rollback in reverse order."""
    try:
        s3_model.delete(s3_suffix)
        LOGGER.info("Invoice properly deleted from S3 during rollback.")
    except Exception as e:
        LOGGER.info("S3 rollback didn't go through: %s", e)
    try:
        invoice_repository.delete(file_id=file_data.file_id, user_id=file_data.user_id)
        LOGGER.info("Invoice properly deleted from database during rollback.")
    except Exception as e:
        LOGGER.info("Database rollback didn't go through: %s", e)
    raise ROLLBACK
