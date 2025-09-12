from pydantic import BaseModel

from invoice_reader.domain.invoice import UUID, InvoiceBase


class InvoiceCreate(BaseModel):
    client_id: UUID
    invoice: InvoiceBase


class InvoiceResponse(BaseModel):
    invoice_id: UUID
    client_id: UUID
    storage_path: str
    data: InvoiceBase


class PagedInvoiceResponse(BaseModel):
    page: int
    per_page: int
    total: int
    data: list[InvoiceResponse]
