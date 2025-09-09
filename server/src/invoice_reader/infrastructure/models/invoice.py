from uuid import UUID
from datetime import date

from sqlmodel import Field, Relationship, SQLModel


class InvoiceModel(SQLModel, table=True):
    __tablename__ = "invoice"

    file_id: UUID = Field(
        primary_key=True,
    )
    user_id: UUID = Field(foreign_key="user.user_id")
    client_id: UUID = Field(foreign_key="client.client_id")
    s3_path: str
    invoice_number: str
    amount_excluding_tax: float
    vat: float
    currency_id: UUID = Field(foreign_key="currency.id") #TODO: Migrate for currency string directly
    description: str
    invoiced_date: date
    paid_date: date | None = None
    uploaded_date: date | None = Field(default_factory=date.today)
    last_updated_date: date | None = Field(default_factory=date.today)

    # client: "ClientModel" = Relationship()
    # currency: "CurrencyModel" = Relationship()
