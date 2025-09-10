from uuid import UUID

from pydantic import BaseModel

from invoice_reader.domain.invoices import Currency, InvoiceData, InvoiceID


class InvoiceCreate(BaseModel):
    client_id: UUID
    currency: Currency
    invoice: InvoiceData


class InvoiceResponse(BaseModel):
    invoice_id: InvoiceID
    client_id: UUID
    storage_path: str
    currency: Currency
    data: InvoiceData


class PagedInvoiceResponse(BaseModel):
    page: int
    per_page: int
    total: int
    data: list[InvoiceResponse]
