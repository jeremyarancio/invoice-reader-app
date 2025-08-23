from uuid import UUID
from pydantic import BaseModel

from invoice_reader.domain.invoices import InvoiceBase


class InvoiceCreate(BaseModel):
    client_id: UUID
    currency_id: UUID
    invoice: InvoiceBase


class InvoiceResponse(BaseModel):
    invoice_id: UUID
    client_id: UUID
    s3_path: str
    currency_id: UUID
    data: InvoiceBase


class PagedInvoiceResponse(BaseModel):
    page: int
    per_page: int
    total: int
    data: list[InvoiceResponse]


class InvoiceUpdate(InvoiceBase):
    currency_id: UUID
    client_id: UUID
