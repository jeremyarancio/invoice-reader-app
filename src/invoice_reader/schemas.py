import os
import uuid
from datetime import date
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class AuthToken(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    user_id: uuid.UUID | None = None
    email: EmailStr
    is_disabled: bool | None = None
    hashed_password: str


class UserCreate(BaseModel):
    password: str = Field(
        ..., min_length=8, description="Password must be at least 8 characters"
    )
    email: EmailStr


class Invoice(BaseModel):
    amount_excluding_tax: float
    vat: Annotated[float, "In percentage: 20, 21, ..."]
    currency: str = "€"
    invoiced_date: date
    invoice_number: str

    def is_complete(self) -> bool:
        return bool(all(self.model_dump().values()))


class Client(BaseModel):
    client_id: uuid.UUID | None = None
    client_name: str
    street_number: int
    street_address: str
    zipcode: int
    city: str
    country: str


class InvoiceCreate(BaseModel):
    invoice: Invoice
    client_id: uuid.UUID


class InvoiceGetResponse(BaseModel):
    file_id: uuid.UUID
    s3_path: str
    data: Invoice


class FileData(BaseModel):
    user_id: uuid.UUID
    filename: str = Field(pattern=r"^.+\.\w{2,3}$", description=".pdf, .png, ...")
    file_id: uuid.UUID | None = Field(default_factory=lambda: uuid.uuid4())

    @property
    def file_format(self):
        return os.path.splitext(self.filename)[-1]


class PagedInvoiceGetResponse(BaseModel):
    page: int
    per_page: int
    total: int
    data: list[InvoiceGetResponse]


class PagedClientResponse(BaseModel):
    page: int
    per_page: int
    total: int
    data: list[Client]
