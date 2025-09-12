from datetime import date

from pydantic import BaseModel

from invoice_reader.domain.invoice import Currency


class ParsedInvoiceData(BaseModel):
    gross_amount: float | None = None
    vat: int | None = None
    issued_date: date | None = None
    invoice_number: str | None = None
    invoice_description: str | None = None
    currency: Currency | None = None


class ParsedClientData(BaseModel):
    client_name: str | None = None
    street_address: str | None = None
    zipcode: str | None = None
    city: str | None = None
    country: str | None = None


class ParserExtraction(BaseModel):
    """Data contract between the parser and our application
    Since values can be missing or unparsable, all fields are optional, meaning
    we can't use the Invoice and Client entities directly.
    """

    invoice: ParsedInvoiceData
    client: ParsedClientData
