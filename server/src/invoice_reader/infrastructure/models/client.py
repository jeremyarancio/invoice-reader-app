from uuid import UUID

from sqlmodel import Field, SQLModel

from invoice_reader.domain.clients import ClientID


class ClientModel(SQLModel, table=True):
    __tablename__ = "client"  # type: ignore

    client_id: ClientID
    user_id: UUID = Field(foreign_key="user.user_id")
    client_name: str
    street_number: int
    street_address: str
    zipcode: int
    city: str
    country: str

    # invoices: list["InvoiceModel"] = Relationship(back_populates="client")
