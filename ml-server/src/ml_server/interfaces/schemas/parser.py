from datetime import date

from pydantic import BaseModel

from ml_server.domain.parser import Currency, ParsedClientData, ParsedData, ParsedInvoiceData


class ParsedInvoiceDataInterface(BaseModel):
    gross_amount: float | None = None
    vat: float | None = None
    issued_date: date | None = None
    invoice_number: str | None = None
    invoice_description: str | None = None
    currency: Currency | None = None

    @classmethod
    def from_parsed_invoice_data(
        cls, parsed_invoice: ParsedInvoiceData
    ) -> "ParsedInvoiceDataInterface":
        return cls(
            gross_amount=parsed_invoice.gross_amount,
            vat=parsed_invoice.vat,
            issued_date=parsed_invoice.issued_date,
            invoice_number=parsed_invoice.invoice_number,
            invoice_description=parsed_invoice.invoice_description,
            currency=parsed_invoice.currency,
        )


class ParsedClientDataInterface(BaseModel):
    client_name: str | None = None
    street_number: str | None = None
    street_address: str | None = None
    zipcode: str | None = None
    city: str | None = None
    country: str | None = None

    @classmethod
    def from_parsed_client_data(
        cls, parsed_client: ParsedClientData
    ) -> "ParsedClientDataInterface":
        return cls(
            client_name=parsed_client.name,
            street_number=parsed_client.street_number,
            street_address=parsed_client.street_address,
            zipcode=parsed_client.zipcode,
            city=parsed_client.city,
            country=parsed_client.country,
        )


class ParsedDataInterface(BaseModel):
    invoice: ParsedInvoiceDataInterface
    client: ParsedClientDataInterface

    @classmethod
    def from_parsed_data(cls, parsed_data: ParsedData) -> "ParsedDataInterface":
        return cls(
            invoice=ParsedInvoiceDataInterface.from_parsed_invoice_data(parsed_data.invoice),
            client=ParsedClientDataInterface.from_parsed_client_data(parsed_data.client),
        )
