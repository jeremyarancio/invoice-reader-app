from pydantic import BaseModel

from invoice_reader.domain.invoice import UUID, Invoice, InvoiceData


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

    @classmethod
    def from_invoice(cls, invoice: Invoice) -> "InvoiceResponse":
        return cls(
            invoice_id=invoice.id_,
            client_id=invoice.client_id,
            storage_path=invoice.storage_path,
            data=invoice.data,
        )


class PagedInvoiceResponse(BaseModel):
    page: int
    per_page: int
    total: int
    invoices: list[InvoiceResponse]
