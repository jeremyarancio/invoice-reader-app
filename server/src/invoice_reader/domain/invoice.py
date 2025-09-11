import os
from datetime import date
from enum import StrEnum
from typing import Annotated, BinaryIO
from uuid import UUID, uuid4

from pydantic import BaseModel, BeforeValidator, Field

from invoice_reader.domain.client import ClientID
from invoice_reader.domain.user import UserID

ACCEPTED_FILE_FORMATS = [".pdf"]


class Currency(StrEnum):
    USD = "usd"
    EUR = "eur"
    GBP = "gbp"


def _is_valid_file_format(filename: str) -> bool:
    if any(filename.endswith(format) for format in ACCEPTED_FILE_FORMATS):
        return True
    raise ValueError(
        f"Invalid file format. Accepted formats are: {ACCEPTED_FILE_FORMATS}"
    )  # TODO: Custom domain exception


class File(BaseModel):
    filename: Annotated[str, BeforeValidator(_is_valid_file_format)]
    file: BinaryIO
    storage_path: str

    @property
    def format(self):
        return os.path.splitext(self.filename)[-1]


class InvoiceID(UUID):
    @classmethod
    def create(cls) -> "InvoiceID":
        return cls(uuid4().hex)


class InvoiceBase(BaseModel):
    invoice_number: str
    gross_amount: float
    vat: Annotated[int, Field(ge=0, le=50)]
    description: Annotated[str, Field(max_length=500)]
    issued_date: date
    paid_date: date | None = None
    currency: Currency


class Invoice(InvoiceBase):
    id_: InvoiceID = Field(default_factory=InvoiceID.create)
    client_id: ClientID
    user_id: UserID
    storage_path: str


class InvoiceUpdate(InvoiceBase):
    client_id: ClientID
