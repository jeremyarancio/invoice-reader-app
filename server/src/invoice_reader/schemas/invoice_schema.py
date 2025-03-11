import uuid
from datetime import date
from typing import Annotated, Literal

from pydantic import BaseModel


class Invoice(BaseModel):
    amount_excluding_tax: float
    vat: Annotated[float, "In percentage: 20, 21, ..."]
    is_paid: bool
    currency: Literal["€", "$"]
    invoiced_date: date
    invoice_number: str


class InvoicePresenter(Invoice):
    s3_path: str | None = None
    file_id: uuid.UUID | None = None


class InvoiceCreate(BaseModel):
    invoice: Invoice
    client_id: uuid.UUID


class InvoiceResponse(BaseModel):
    invoice_id: uuid.UUID
    client_id: uuid.UUID
    s3_path: str
    data: Invoice


class PagedInvoiceResponse(BaseModel):
    page: int
    per_page: int
    total: int
    data: list[InvoiceResponse]


class InvoiceUpdate(Invoice):
    """Let's see how it can be improved later on."""
