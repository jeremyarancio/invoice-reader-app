from datetime import date, datetime
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ValidationInfo, field_validator

from ml_server.domain.parser import (
    Currency,
    ParsedClientData,
    ParsedData,
    ParsedInvoiceData,
    ParserPrediction,
)


def _is_positive_float(value) -> float | None:
    return value if isinstance(value, float | int) and value >= 0 else None


def _is_valid_currency(value: str) -> str | None:
    if value.upper() in Currency.__members__:
        return value.upper()
    return None


def _is_valid_date(value) -> date | None:
    if isinstance(value, date):
        return value
    else:
        try:
            return datetime.strptime(value, "%d/%m/%Y").date()
        except (ValueError, TypeError):
            return None


class ParsedInvoiceDataSchema(BaseModel):
    gross_amount: Annotated[float | None, BeforeValidator(_is_positive_float)] = None
    vat: Annotated[float | None, BeforeValidator(_is_positive_float)] = None
    issued_date: Annotated[date | None, BeforeValidator(_is_valid_date)] = None
    due_date: date | None = None
    invoice_number: str | None = None
    invoice_description: str | None = None
    currency: Annotated[Currency | None, BeforeValidator(_is_valid_currency)] = None

    @field_validator("due_date", mode="before")
    @classmethod
    def validate_due_date(cls, value, info: ValidationInfo) -> date | None:
        _date = _is_valid_date(value)
        if _date:
            issued_date = info.data.get("issued_date")
            if issued_date and _date > issued_date:
                return _date
            return None


class ParsedClientDataSchema(BaseModel):
    name: str | None = None
    street_address_number: str | None = None
    street_address: str | None = None
    zipcode: str | None = None
    city: str | None = None
    country: str | None = None


class ParsedDataSchema(BaseModel):
    invoice: ParsedInvoiceDataSchema
    client: ParsedClientDataSchema

    def to_prediction(self, model_name: str) -> ParserPrediction:
        return ParserPrediction(
            model_name=model_name,
            data=ParsedData(
                invoice=ParsedInvoiceData(
                    gross_amount=self.invoice.gross_amount,
                    vat=self.invoice.vat,
                    issued_date=self.invoice.issued_date,
                    due_date=self.invoice.due_date,
                    invoice_number=self.invoice.invoice_number,
                    invoice_description=self.invoice.invoice_description,
                    currency=self.invoice.currency,
                ),
                client=ParsedClientData(
                    name=self.client.name,
                    street_number=self.client.street_address_number,
                    street_address=self.client.street_address,
                    zipcode=self.client.zipcode,
                    city=self.client.city,
                    country=self.client.country,
                ),
            ),
        )
