import os
from datetime import date
from enum import StrEnum
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator

from invoice_reader.domain.exceptions import (
    AmountsCurrencyMismatchException,
    InvalidFileFormatException,
)

ACCEPTED_FILE_FORMATS = [".pdf"]


class Currency(StrEnum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CZK = "CZK"


type CurrencyAmounts = dict[Currency, float]

type ExchangeRates = dict[Currency, float]


class Amount(BaseModel):
    currency_amounts: CurrencyAmounts
    base_currency: Currency

    @property
    def base_amount(self) -> float:
        return self.currency_amounts.get(self.base_currency, 0)

    @classmethod
    def from_rate_exchanges(
        cls, exchange_rates: ExchangeRates, base_amount: float, base_currency: Currency
    ) -> "Amount":
        currency_amounts = {cur: rate * base_amount for cur, rate in exchange_rates.items()}
        return cls(currency_amounts=currency_amounts, base_currency=base_currency)

    def __add__(self, other: "Amount") -> "Amount":
        """Add two amounts together across all currencies."""
        if set(self.currency_amounts.keys()) != set(other.currency_amounts.keys()):
            raise AmountsCurrencyMismatchException("Cannot add amounts with different currencies")
        new_currency_amounts = {
            currency: self.currency_amounts[currency] + other.currency_amounts[currency]
            for currency in self.currency_amounts
        }
        return Amount(
            currency_amounts=new_currency_amounts,
            base_currency=self.base_currency,
        )


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
    vat: Annotated[int, Field(ge=0, le=50)]
    description: Annotated[str, Field(max_length=500)]
    issued_date: date
    paid_date: date | None = None


class Invoice(BaseModel):
    id_: UUID = Field(default_factory=uuid4)
    client_id: UUID
    user_id: UUID
    storage_path: str
    data: InvoiceData
    gross_amount: Amount
