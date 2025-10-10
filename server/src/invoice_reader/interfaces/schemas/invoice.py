from pydantic import BaseModel

from invoice_reader.domain.invoice import UUID, Currency, Invoice, InvoiceData


class InvoiceInterfaceData(InvoiceData):
    gross_amount: float
    currency: Currency


class InvoiceCreate(BaseModel):
    client_id: UUID
    data: InvoiceInterfaceData


class InvoiceUpdate(BaseModel):
    client_id: UUID
    data: InvoiceInterfaceData


class InvoiceResponse(BaseModel):
    invoice_id: UUID
    client_id: UUID
    storage_path: str
    data: InvoiceInterfaceData

    @classmethod
    def from_invoice(cls, invoice: Invoice) -> "InvoiceResponse":
        return cls(
            invoice_id=invoice.id_,
            client_id=invoice.client_id,
            storage_path=invoice.storage_path,
            data=InvoiceInterfaceData(
                invoice_number=invoice.data.invoice_number,
                vat=invoice.data.vat,
                description=invoice.data.description,
                issued_date=invoice.data.issued_date,
                paid_date=invoice.data.paid_date,
                gross_amount=invoice.gross_amount.base_amount,
                currency=invoice.gross_amount.base_currency,
            ),
        )


class PagedInvoiceResponse(BaseModel):
    page: int
    per_page: int
    total: int
    invoices: list[InvoiceResponse]
