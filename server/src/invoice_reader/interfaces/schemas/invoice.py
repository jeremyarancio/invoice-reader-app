from pydantic import BaseModel

from invoice_reader.domain.client import ClientID
from invoice_reader.domain.invoice import Currency, InvoiceBase, InvoiceID


class InvoiceCreate(BaseModel):
    client_id: ClientID
    currency: Currency
    invoice: InvoiceBase


class InvoiceResponse(BaseModel):
    invoice_id: InvoiceID
    client_id: ClientID
    storage_path: str
    data: InvoiceBase


class PagedInvoiceResponse(BaseModel):
    page: int
    per_page: int
    total: int
    data: list[InvoiceResponse]
