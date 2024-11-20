from abc import ABC, abstractmethod
from typing import TypeVar
import uuid

import sqlmodel

from invoice_reader import schemas
from invoice_reader import models
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


class InvoiceRepository(Repository[schemas.InvoiceSchema]):
	def __init__(self, session: sqlmodel.Session):
		self.session = session

	def add(self, id_: uuid.UUID, invoice: schemas.InvoiceSchema, s3_path: str) -> str:
		is_existing_invoice = self.session.exec(
			sqlmodel.select(models.InvoiceModel)
			.where(models.InvoiceModel.file_id == id_)
		).one_or_none()
		if not is_existing_invoice:
			invoice_model = models.InvoiceModel(file_id=id_, s3_path=s3_path, **invoice.model_dump())
			self.session.add(invoice_model)
			self.session.commit()
			self.session.refresh(invoice_model)
			LOGGER.info("Invoice %s add to database. Metadata: %s", id_, invoice)
		else:
			LOGGER.info("Invoice already existing. No change was performed.")

	def update(self, id_: str, invoice: schemas.InvoiceSchema) -> None:
		invoice_model = self.session.exec(
			sqlmodel.select(models.InvoiceModel).where(models.InvoiceModel.file_id == id_)
		).one()
		invoice_model.sqlmodel_update(invoice)
		self.session.add(invoice_model)
		self.session.commit()
		self.session.refresh(invoice_model)
		LOGGER.info("Existing invoice %s data updated with new data: %s", id_, invoice)

	def get(self, id_: str) -> schemas.InvoiceSchema:
		invoice_model = self.session.exec(sqlmodel.select(models.InvoiceModel.file_id == id_)).one()
		invoice = schemas.InvoiceSchema.model_validate(invoice_model)
		LOGGER.info("Invoice data retrieved from database: %s", invoice)
		return invoice

	def delete(self, id_: str) -> None:
		invoice_model = self.session.exec(sqlmodel.select(models.InvoiceModel.file_id == id_)).one()
		self.session.delete(invoice_model)
		self.session.commit()
		LOGGER.info("Invoice %s deleted from database.", id_)

	def get_all(self, limit: int = 10) -> list[schemas.InvoiceSchema]:
		invoice_models = self.session.exec(sqlmodel.select(models.InvoiceModel).limit(limit)).all()
		invoices = [
			schemas.InvoiceSchema(**invoice_model.model_dump()) for invoice_model in invoice_models
		]
		LOGGER("List of invoices returned from database: %s", invoices)
		return invoice_models
