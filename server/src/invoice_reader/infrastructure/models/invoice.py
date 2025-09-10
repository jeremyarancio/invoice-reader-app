from datetime import date
from uuid import UUID

from sqlmodel import Field, SQLModel

from invoice_reader.domain.invoices import Currency, InvoiceID


class InvoiceModel(SQLModel, table=True):
    __tablename__ = "invoice"  # type: ignore

    invoice_id: InvoiceID = Field(
        primary_key=True,
    )
    user_id: UUID = Field(foreign_key="user.user_id")
    client_id: UUID = Field(foreign_key="client.client_id")
    storage_path: str
    invoice_number: str
    amount_excluding_tax: float
    vat: int
    currency: Currency
    description: str
    invoiced_date: date
    paid_date: date | None = None
    uploaded_date: date | None = Field(default_factory=date.today)
    last_updated_date: date | None = Field(default_factory=date.today)

    # client: "ClientModel" = Relationship()
    # currency: "CurrencyModel" = Relationship()
