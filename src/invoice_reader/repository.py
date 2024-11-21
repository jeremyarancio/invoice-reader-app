from abc import ABC, abstractmethod
from typing import TypeVar

import sqlmodel

from invoice_reader.schemas import InvoiceSchema, UserSchema
from invoice_reader.models import InvoiceModel, UserModel
from invoice_reader.utils.logger import get_logger


LOGGER = get_logger(__name__)

T = TypeVar("T")


class Repository[T](ABC):
	@abstractmethod
	def get(self, id_: str) -> T:
		raise NotImplementedError

	@abstractmethod
	def delete(self, id_: str) -> None:
		raise NotImplementedError

	@abstractmethod
	def update(self, **kwargs: object) -> None:
		raise NotImplementedError

	@abstractmethod
	def add(self, id_: str, **kwargs: object) -> None:
		raise NotImplementedError

	@abstractmethod
	def get_all(self, limit: int) -> list[T]:
		raise NotImplementedError


class InvoiceRepository(Repository[InvoiceSchema]):
	def __init__(self, session: sqlmodel.Session):
		self.session = session

	def add(self, id_: str, user_id: str, invoice_data: InvoiceSchema, s3_path: str) -> str:
		invoice_model = InvoiceModel(
			file_id=id_, user_id=user_id, s3_path=s3_path, **invoice_data.model_dump()
		)
		self.session.add(invoice_model)
		self.session.commit()
		self.session.refresh(invoice_model)
		LOGGER.info("Invoice %s added to database. Metadata: %s", id_, invoice_model)

	def update(self, id_: str, invoice_data: InvoiceSchema) -> None:
		invoice_model = self.session.exec(
			sqlmodel.select(InvoiceModel).where(InvoiceModel.file_id == id_)
		).one()
		invoice_model.sqlmodel_update(invoice_data)
		self.session.add(invoice_model)
		self.session.commit()
		self.session.refresh(invoice_model)
		LOGGER.info("Existing invoice %s data updated with new data: %s", id_, invoice_data)

	def get(self, id_: str) -> InvoiceSchema:
		invoice_model = self.session.exec(sqlmodel.select(InvoiceModel.file_id == id_)).one()
		invoice = InvoiceSchema.model_validate(invoice_model)
		LOGGER.info("Invoice data retrieved from database: %s", invoice)
		return invoice

	def delete(self, id_: str) -> None:
		invoice_model = self.session.exec(sqlmodel.select(InvoiceModel.file_id == id_)).one()
		self.session.delete(invoice_model)
		self.session.commit()
		LOGGER.info("Invoice %s deleted from database.", id_)

	def get_all(self, limit: int = 10) -> list[InvoiceSchema]:
		invoice_models = self.session.exec(sqlmodel.select(InvoiceModel).limit(limit)).all()
		invoices = [InvoiceSchema(**invoice_model.model_dump()) for invoice_model in invoice_models]
		LOGGER("List of invoices returned from database: %s", invoices)
		return invoice_models


class UserRepository(Repository):
	def __init__(self, session: sqlmodel.Session):
		self.session = session

	def add(self, user_data: UserSchema):
		user_model = UserModel(**user_data.model_dump())
		self.session.add(user_model)
		self.session.commit()
		self.session.refresh(user_model)
		LOGGER.info("New user added to database: %s", user_model)

	def update(self, id_: str, user_data: UserSchema) -> None:
		user_model = self.session.exec(
			sqlmodel.select(UserModel).where(UserModel.user_id == id_)
		).one()
		user_model.sqlmodel_update(user_model)
		self.session.add(user_model)
		self.session.commit()
		self.session.refresh(user_model)
		LOGGER.info("Existing user %s udpated: %s", id_, user_model)

	def get(self, id_: str) -> InvoiceSchema:
		user_model = self.session.exec(sqlmodel.select(UserModel.file_id == id_)).one()
		invoice = InvoiceSchema.model_validate(user_model)
		LOGGER.info("Invoice data retrieved from database: %s", invoice)
		return invoice

	def delete(self, id_: str) -> None:
		user_model = self.session.exec(sqlmodel.select(UserModel.file_id == id_)).one()
		self.session.delete(user_model)
		self.session.commit()
		LOGGER.info("Invoice %s deleted from database.", id_)

	def get_all(self, limit: int = 10) -> list[InvoiceSchema]:
		user_models = self.session.exec(sqlmodel.select(UserModel).limit(limit)).all()
		invoices = [InvoiceSchema(**user_model.model_dump()) for user_model in user_models]
		LOGGER("List of invoices returned from database: %s", invoices)
		return user_models
