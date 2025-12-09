from datetime import date

from pydantic import BaseModel

from invoice_reader.domain.client import ClientData
from invoice_reader.domain.invoice import Currency, InvoiceData


class ParsedInvoiceData(BaseModel):
    gross_amount: float | None = None
    vat: float | None = None
    issued_date: date | None = None
    invoice_number: str | None = None
    invoice_description: str | None = None
    currency: Currency | None = None

    def to_invoice_data(self) -> InvoiceData:
        return InvoiceData(
            gross_amount=self.gross_amount if self.gross_amount else 0,
            vat=self.vat if self.vat else 0,
            issued_date=self.issued_date if self.issued_date else date.today(),
            invoice_number=self.invoice_number if self.invoice_number else "",
            description=self.invoice_description if self.invoice_description else "",
            currency=self.currency if self.currency else Currency.USD,
        )


class ParsedClientData(BaseModel):
    client_name: str | None = None
    street_number: str | None = None
    street_address: str | None = None
    zipcode: str | None = None
    city: str | None = None
    country: str | None = None

    def to_client_data(self) -> ClientData:
        return ClientData(
            client_name=self.client_name if self.client_name else "",
            street_number=self.street_number if self.street_number else "",
            street_address=self.street_address if self.street_address else "",
            zipcode=self.zipcode if self.zipcode else "",
            city=self.city if self.city else "",
            country=self.country if self.country else "",
        )


class ParsedData(BaseModel):
    invoice: ParsedInvoiceData
    client: ParsedClientData
