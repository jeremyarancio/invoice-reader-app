from sqlmodel import Field, SQLModel  # type: ignore

from invoice_reader.domain.client import ClientID
from invoice_reader.domain.user import UserID


class ClientModel(SQLModel, table=True):
    __tablename__ = "client"  # type: ignore

    client_id: ClientID
    user_id: UserID = Field(foreign_key="user.user_id")
    client_name: str
    street_number: int
    street_address: str
    zipcode: int
    city: str
    country: str

    # invoices: list["InvoiceModel"] = Relationship(back_populates="client")
