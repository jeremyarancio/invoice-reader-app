import uuid
from typing import BinaryIO

import sqlmodel

from invoice_reader import settings
from invoice_reader.core import storage
from invoice_reader.models import S3
from invoice_reader.repository import InvoiceRepository, UserRepository
from invoice_reader.schemas import FileData, InvoiceSchema, UserSchema


def submit(
	user_id: uuid.UUID,
	file: BinaryIO,
	filename: str,
	invoice_data: InvoiceSchema,
	session: sqlmodel.Session,
):
	file_data = FileData(user_id=user_id, filename=filename)
	s3_model = S3.init(
		bucket=settings.S3_BUCKET,
		file_data=file_data
	)
	invoice_repository = InvoiceRepository(session=session)
	storage.store(
		file=file,
		file_data=file_data,
		invoice_data=invoice_data,
		s3_model=s3_model,
		invoice_repository=invoice_repository,
	)


def extract(file: BinaryIO) -> InvoiceSchema:
	raise NotImplementedError


def get_user(token: str):
	raise NotImplementedError


def register_user(user: UserSchema, session: sqlmodel.Session) -> None:
	user_repository = UserRepository(session=session)
	user_repository.add(user)


def get_user_by_username(username: str, session: sqlmodel.Session) -> UserSchema:
	user_repository = UserRepository(session=session)
	user = user_repository.get_by_username(username)
	return user


def get_user_by_email(email: str, session: sqlmodel.Session) -> UserSchema | None:
	user_repository = UserRepository(session=session)
	user = user_repository.get_user_by_email(email=email)
	return user


def add_user(user: UserSchema, session: sqlmodel.Session) -> None:
	user_repository = UserRepository(session=session)
	user = user_repository.add(user=user)