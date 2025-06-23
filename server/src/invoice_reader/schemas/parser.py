from datetime import date

from pydantic import BaseModel


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
    currency: str | None = None


class CompanyDataExtraction(BaseModel):
    name: str | None = None
    address: Address | None = None


class InvoiceExtraction(BaseModel):
    invoice: InvoiceDataExtraction
    client: CompanyDataExtraction
    seller: CompanyDataExtraction
