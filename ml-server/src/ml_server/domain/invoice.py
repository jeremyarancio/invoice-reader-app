from datetime import date, datetime
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ValidationInfo, field_validator

CURRENCIES = ["USD", "EUR", "GBP"]


def _is_positive_integer(value: int | None) -> int | None:
    return int(value) if value and value >= 0 else None


def _is_positive_float(value: float | None) -> float | None:
    return float(value) if value and value >= 0 else None


def _is_valid_currency(value: str | None) -> str | None:
    if value and value.upper() in CURRENCIES:
        return value.upper()
    return None


def _is_valid_date(value: str | date | None) -> date | None:
    if value:
        if isinstance(value, date):
            return value
        else:
            try:
                return datetime.strptime(value, "%d/%m/%Y").date()
            except (ValueError, TypeError):
                return None
    return None


class Address(BaseModel):
    street_address: str | None = None
    zipcode: str | None = None
    city: str | None = None
    country: str | None = None


class Invoice(BaseModel):
    gross_amount: Annotated[float | None, BeforeValidator(_is_positive_float)] = None
    vat: Annotated[int | None, BeforeValidator(_is_positive_integer)] = None
    issued_date: Annotated[date | None, BeforeValidator(_is_valid_date)] = None
    due_date: date | None = None
    invoice_number: str | None = None
    invoice_description: str | None = None
    currency: Annotated[str | None, BeforeValidator(_is_valid_currency)] = None

    @field_validator("due_date", mode="before")
    @classmethod
    def validate_due_date(cls, value, info: ValidationInfo) -> date | None:
        _date = _is_valid_date(value)
        if _date:
            issued_date = info.data.get("issued_date")
            if issued_date and _date > issued_date:
                return _date
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
