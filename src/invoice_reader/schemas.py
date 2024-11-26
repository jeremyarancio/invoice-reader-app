import os
import uuid
from datetime import date
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class User(BaseModel):
    user_id: uuid.UUID | None = None
    username: str
    email: EmailStr
    is_disabled: bool | None = None
    hashed_password: str


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=30, pattern="^[a-zA-Z0-9_]+$")
    password: str = Field(
        ..., min_length=8, description="Password must be at least 8 characters"
    )
    email: EmailStr


class InvoiceData(BaseModel):
    client_name: str
    amount_excluding_tax: float
    vat: Annotated[float, "In percentage: 20, 21, ..."]
    currency: str = "€"
    invoiced_date: date
    invoice_number: str
    street_number: int
    street_address: str
    zipcode: int
    city: str
    country: str

    def is_complete(self) -> bool:
        return bool(all(self.model_dump().values()))


class FileData(BaseModel):
    user_id: uuid.UUID
    filename: str = Field(pattern=r"^\w+\.\w{2,3}$", description=".pdf, .png, ...")
    file_id: uuid.UUID | None = Field(default_factory=lambda: uuid.uuid4())

    @property
    def file_format(self):
        return os.path.splitext(self.filename)[-1]
