import os
from typing import Annotated
from datetime import date
import uuid

from pydantic import BaseModel, Field


class ClientAdresseSchema(BaseModel):
	street_number: int
	street_name: str
	zipcode: int
	city: str
	country: str


class RevenuSchema(BaseModel):
	excluding_tax: float = None
	vat: Annotated[float, "In percentage: 20, 21, ..."] = None
	currency: str = "€"


class InvoiceSchema(BaseModel):
	client_name: str = None
	client_adresse: ClientAdresseSchema = None
	revenu: RevenuSchema = None
	invoiced_date: date = None
	number: str = None

	def is_complete(self) -> bool:
		if all(self.model_dump().values()):
			return True
		return False


class FileData(BaseModel):
	user_id: str
	filename: str = Field(pattern=r"^\w+\.\w{2,3}$", description=".pdf, .png, ...")

	@property
	def file_format(self):
		return os.path.splitext(self.filename)[-1]
