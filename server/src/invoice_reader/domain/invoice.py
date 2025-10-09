import os
from datetime import date
from enum import StrEnum
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator

from invoice_reader.domain.exceptions import InvalidFileFormatException

ACCEPTED_FILE_FORMATS = [".pdf"]


class Currency(StrEnum):
    USD = "usd"
    EUR = "eur"
    GBP = "gbp"


class File(BaseModel):
    filename: str
    file: bytes
    storage_path: str

    @field_validator("filename")
    @classmethod
    def validate_file_format(cls, v: str) -> str:
        file_extension = os.path.splitext(v)[-1].lower()
        if file_extension not in ACCEPTED_FILE_FORMATS:
            raise InvalidFileFormatException(
                f"""Invalid file format '{file_extension}'. 
                Accepted formats: {", ".join(ACCEPTED_FILE_FORMATS)}"""
            )
        return v

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
