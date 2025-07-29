from datetime import date
from enum import StrEnum

from pydantic import BaseModel, field_validator


class Currency(StrEnum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"


class Address(BaseModel):
    street_address: str | None = None
    zipcode: str | None = None
    city: str | None = None
    country: str | None = None


class Invoice(BaseModel):
    gross_amount: float | None = None
    vat: int | None = None
    issued_date: date | None = None
    invoice_number: str | None = None
    invoice_description: str | None = None
    currency: Currency | None = None

    @field_validator("vat", mode="before")
    @classmethod
    def validate_vat(cls, v):
        if v is None or v >= 0:
            return v
        return None


class Client(BaseModel):
    name: str | None = None
    address: Address | None = None


class Seller(BaseModel):
    name: str | None = None
    address: Address | None = None


class InvoiceExtraction(BaseModel):
    invoice: Invoice
    client: Client
    seller: Seller
