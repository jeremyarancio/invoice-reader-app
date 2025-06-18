import uuid
from datetime import date
from typing import Annotated

from pydantic import BaseModel


class InvoiceBase(BaseModel):
    gross_amount: float
    vat: Annotated[float, "In percentage: 20, 21, ..."]
    invoiced_date: date
    paid_date: date | None = None
    invoice_number: str
    description: str


class Invoice(InvoiceBase):
    s3_path: str | None = None
    file_id: uuid.UUID | None = None
    client_id: uuid.UUID
    currency_id: uuid.UUID


class InvoiceCreate(BaseModel):
    client_id: uuid.UUID
    currency_id: uuid.UUID
    invoice: InvoiceBase


class InvoiceResponse(BaseModel):
    invoice_id: uuid.UUID
    client_id: uuid.UUID
    s3_path: str
    currency_id: uuid.UUID
    data: InvoiceBase


class PagedInvoiceResponse(BaseModel):
    page: int
    per_page: int
    total: int
    data: list[InvoiceResponse]


class InvoiceUpdate(InvoiceBase):
    currency_id: uuid.UUID
    client_id: uuid.UUID
