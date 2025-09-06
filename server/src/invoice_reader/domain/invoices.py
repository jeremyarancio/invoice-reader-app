from enum import StrEnum
import os
from uuid import UUID, uuid4
from datetime import date
from typing import Annotated

from pydantic import BaseModel, Field, BeforeValidator


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
    storage_path: Annotated[
        str, Field(pattern=r"^s3://.+/.+$")
    ]  # NOTE: What if not S3?

    @property
    def format(self):
        return os.path.splitext(self.filename)[-1]


class InvoiceID(UUID):
    pass


class Invoice(BaseModel):
    id_: Annotated[InvoiceID, Field(default_factory=uuid4)]
    client_id: UUID
    user_id: UUID
    file: File
    currency: Currency
    invoice_number: str
    gross_amount: float
    vat: Annotated[int, Field(ge=0, le=50)]
    description: Annotated[str, Field(max_length=500)]
    issued_date: date
    paid_date: date | None = None
