import os
from datetime import date
from enum import StrEnum
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

ACCEPTED_FILE_FORMATS = [".pdf"]


class Currency(StrEnum):
    USD = "usd"
    EUR = "eur"
    GBP = "gbp"


class File(BaseModel):
    filename: Annotated[
        str, Field(pattern=rf".+({'|'.join([fmt.lstrip('.') for fmt in ACCEPTED_FILE_FORMATS])})$")
    ]
    file: bytes
    storage_path: str

    @property
    def format(self):
        return os.path.splitext(self.filename)[-1]


class InvoiceData(BaseModel):
    invoice_number: str
    gross_amount: float
    vat: Annotated[int, Field(ge=0, le=50)]
    description: Annotated[str, Field(max_length=500)]
    issued_date: date
    paid_date: date | None = None
    currency: Currency


class Invoice(BaseModel):
    id_: UUID = Field(default_factory=uuid4)
    client_id: UUID
    user_id: UUID
    storage_path: str
    data: InvoiceData
