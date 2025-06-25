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


class InvoiceModel(SQLModel, table=True):
    __tablename__ = "invoice"

    file_id: uuid.UUID = Field(
        primary_key=True,
        description="file_id is required since manually added to store both in S3 and in the DB",
    )
    user_id: uuid.UUID = Field(foreign_key="user.user_id")
    client_id: uuid.UUID = Field(foreign_key="client.client_id")
    s3_path: str
    invoice_number: str
    amount_excluding_tax: float
    vat: float
    currency_id: uuid.UUID = Field(foreign_key="currency.id")
    description: str
    invoiced_date: datetime.date
    paid_date: datetime.date | None = None
    uploaded_date: datetime.date | None = Field(default_factory=datetime.datetime.now)
    last_updated_date: datetime.date | None = Field(
        default_factory=datetime.datetime.now
    )

    client: "ClientModel" = Relationship()
    currency: "CurrencyModel" = Relationship()


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
