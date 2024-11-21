import os
from typing import Annotated
from datetime import date
import uuid

from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
	user_id: uuid.UUID | None = Field(
		default=None,
		description="Only for debugging. SQLModel takes charge of generating it automatically",
	)
	email: EmailStr


class InvoiceSchema(BaseModel):
	client_name: str
	amount_excluding_tax: float
	vat: Annotated[float, "In percentage: 20, 21, ..."]
	currency: str = "€"
	invoiced_date: date
	invoice_number: str
	street_number: int
	street_address: str
	zipcode: int
	city: str
	country: str

	def is_complete(self) -> bool:
		if all(self.model_dump().values()):
			return True
		return False


class FileData(BaseModel):
	user_id: uuid.UUID
	filename: str = Field(pattern=r"^\w+\.\w{2,3}$", description=".pdf, .png, ...")
	file_id: uuid.UUID | None = Field(default_factory=lambda: uuid.uuid4())

	@property
	def file_format(self):
		return os.path.splitext(self.filename)[-1]
