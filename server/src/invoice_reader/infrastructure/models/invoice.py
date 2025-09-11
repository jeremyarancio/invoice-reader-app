from datetime import date

from sqlmodel import Field, SQLModel  # type: ignore

from invoice_reader.domain.client import ClientID
from invoice_reader.domain.invoice import Currency, InvoiceID
from invoice_reader.domain.user import UserID


class InvoiceModel(SQLModel, table=True):
    __tablename__ = "invoice"  # type: ignore

    invoice_id: InvoiceID = Field(primary_key=True)
    user_id: UserID = Field(foreign_key="user.user_id")
    client_id: ClientID = Field(foreign_key="client.client_id")
    storage_path: str
    invoice_number: str
    gross_amount: float
    vat: int
    currency: Currency
    description: str
    invoiced_date: date
    paid_date: date | None = None
    uploaded_date: date | None = Field(default_factory=date.today)
    last_updated_date: date | None = Field(default_factory=date.today)

    # client: "ClientModel" = Relationship()
    # currency: "CurrencyModel" = Relationship()
