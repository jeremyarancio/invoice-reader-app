from pydantic import BaseModel

from invoice_reader.domain.invoice import UUID, InvoiceData


class InvoiceCreate(BaseModel):
    client_id: UUID
    data: InvoiceData


class InvoiceUpdate(BaseModel):
    client_id: UUID
    data: InvoiceData


class InvoiceResponse(BaseModel):
    invoice_id: UUID
    client_id: UUID
    storage_path: str
    data: InvoiceData


class PagedInvoiceResponse(BaseModel):
    page: int
    per_page: int
    total: int
    invoices: list[InvoiceResponse]
