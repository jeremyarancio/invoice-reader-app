from uuid import UUID
from pydantic import BaseModel

from invoice_reader.domain.invoices import InvoiceData, InvoiceID


class InvoiceCreate(BaseModel):
    client_id: UUID
    currency_id: UUID
    invoice: InvoiceData


class InvoiceResponse(BaseModel):
    invoice_id: InvoiceID
    client_id: UUID
    s3_path: str
    currency_id: UUID
    data: InvoiceData


class PagedInvoiceResponse(BaseModel):
    page: int
    per_page: int
    total: int
    data: list[InvoiceResponse]


class InvoiceUpdate(InvoiceResponse):
    client_id: UUID
    data: InvoiceData