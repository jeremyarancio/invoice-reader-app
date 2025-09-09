import datetime
import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from invoice_reader.utils.logger import get_logger

LOGGER = get_logger(__name__)


class UserModel(SQLModel, table=True):
    __tablename__ = "user"

    user_id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr
    is_disabled: bool = Field(default=False)
    hashed_password: str


class ClientModel(SQLModel, table=True):
    __tablename__ = "client"

    client_id: uuid.UUID | None = Field(primary_key=True, default_factory=uuid.uuid4)
    user_id: uuid.UUID = Field(foreign_key="user.user_id")
    client_name: str
    street_number: int
    street_address: str
    zipcode: int
    city: str
    country: str

    invoices: list["InvoiceModel"] = Relationship(back_populates="client")


class CurrencyModel(SQLModel, table=True):
    __tablename__ = "currency"

    id: uuid.UUID | None = Field(primary_key=True, default_factory=uuid.uuid4)
    currency: str

    invoices: list["InvoiceModel"] = Relationship(back_populates="currency")
