from typing import BinaryIO

from invoice_reader.core import storage
from invoice_reader.schemas import InvoiceMetadata
from invoice_reader import settings
from invoice_reader import schemas


def submit(user_id: str, file: BinaryIO, filename: str, metadata: InvoiceMetadata):
	file_data = schemas.FileData(user_id=user_id, filename=filename)
	storage.store(
		file=file,
		file_data=file_data,
		metadata=metadata,
		bucket=settings.S3_BUCKET,
	)


def extract(file: BinaryIO) -> InvoiceMetadata:
	raise NotImplementedError


def get_user_id(token: str):
	raise NotImplementedError
