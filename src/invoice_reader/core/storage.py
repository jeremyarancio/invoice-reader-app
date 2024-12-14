from typing import BinaryIO

from invoice_reader.models import S3
from invoice_reader.repository import InvoiceRepository, Repository
from invoice_reader.schemas import FileData, InvoiceCreate
from invoice_reader.utils.logger import get_logger

LOGGER = get_logger()


def store(
    file: BinaryIO,
    file_data: FileData,
    invoice_data: InvoiceCreate,
    invoice_repository: Repository,
    s3_model: S3,
) -> None:
    store_invoice_data(
        file_data=file_data,
        invoice_repository=invoice_repository,
        invoice_data=invoice_data,
        s3_path=s3_model.path,
    )
    store_file(file=file, s3_model=s3_model)
    # TODO: Rollback


def store_file(file: BinaryIO, s3_model: S3) -> None:
    s3_model.store(file=file)
    LOGGER.info("File stored succesfully at %s", s3_model.path)


def store_invoice_data(
    file_data: FileData,
    invoice_data: InvoiceCreate,
    s3_path: str,
    invoice_repository: InvoiceRepository,
) -> str:
    invoice_repository.add(
        id_=file_data.file_id,
        user_id=file_data.user_id,
        invoice_data=invoice_data.invoice,
        client_id=invoice_data.client_id,
        s3_path=s3_path,
    )
