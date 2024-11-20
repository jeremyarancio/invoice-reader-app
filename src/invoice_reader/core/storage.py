from typing import BinaryIO
import sqlmodel
import uuid

from invoice_reader.schemas import InvoiceSchema
from invoice_reader.models import S3
from invoice_reader.utils.logger import get_logger
from invoice_reader.schemas import FileData
from invoice_reader.repository import InvoiceRepository

LOGGER = get_logger()


def store(
	file: BinaryIO,
	file_data: FileData,
	invoice: InvoiceSchema,
	bucket: str | None,
	session: sqlmodel.Session,
) -> None:
	if not bucket:
		raise ValueError("S3 bucket name was not found as environment variable.")
	try:
		s3_model = S3.init(bucket=bucket, file_data=file_data)
		invoice_repository = InvoiceRepository(session=session)
		store_invoice_data(
			file_id=file_data.file_id,
			invoice_repository=invoice_repository,
			invoice_schema=invoice,
			s3_path=s3_model.path,
		)
		store_file(file=file, s3_model=s3_model)
	except Exception as e:
		LOGGER.error(e)
		# TODO: Rollback


def store_file(file: BinaryIO, s3_model: S3) -> None:
	s3_model.store(file=file)
	LOGGER.info("File stored succesfully at %s", s3_model.path)


def store_invoice_data(
	file_id: uuid.UUID,
	invoice_schema: InvoiceSchema,
	s3_path: str,
	invoice_repository: InvoiceRepository,
) -> str:
	invoice_repository.add(id_=file_id, invoice=invoice_schema, s3_path=s3_path)
