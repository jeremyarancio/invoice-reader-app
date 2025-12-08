from dataclasses import dataclass
from datetime import date
from enum import StrEnum


class Currency(StrEnum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CZK = "CZK"


@dataclass
class ParsedClientData:
    name: str | None
    street_number: str | None
    street_address: str | None
    zipcode: str | None
    city: str | None
    country: str | None


@dataclass
class ParsedInvoiceData:
    gross_amount: float | None
    vat: float | None
    issued_date: date | None
    due_date: date | None
    invoice_number: str | None
    invoice_description: str | None
    currency: Currency | None


@dataclass
class ParsedData:
    invoice: ParsedInvoiceData
    client: ParsedClientData


@dataclass
class ParserPrediction:
    model_name: str
    data: ParsedData
