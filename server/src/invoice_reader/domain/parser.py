from datetime import date
from uuid import UUID

from pydantic import BaseModel, field_validator


class Address(BaseModel):
    street_address: str | None = None
    zipcode: str | None = None
    city: str | None = None
    country: str | None = None


class InvoiceDataExtraction(BaseModel):
    gross_amount: float | None = None
    vat: int | None = None
    issued_date: date | None = None
    invoice_number: str | None = None
    invoice_description: str | None = None
    currency_id: UUID | None = None

    @field_validator("vat", mode="before")
    @classmethod
    def validate_vat(cls, v: float | int | None) -> int | None:
        if v is None or v >= 0:
            return int(v)
        return None


class ClientDataExtraction(BaseModel):
    client_id: UUID | None = None
    address: Address | None = None


class SellerDataExtraction(BaseModel):
    name: str | None = None
    address: Address | None = None


class InvoiceExtraction(BaseModel):
    invoice: InvoiceDataExtraction
    client: ClientDataExtraction
    seller: SellerDataExtraction
