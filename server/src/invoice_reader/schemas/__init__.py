import os
import uuid

from pydantic import BaseModel, Field

from .clients import *
from .invoices import *
from .users import *


class AuthToken(BaseModel):
    access_token: str
    token_type: str


class FileData(BaseModel):
    user_id: uuid.UUID
    filename: str = Field(pattern=r"^.+\.\w{2,3}$", description=".pdf, .png, ...")
    file_id: uuid.UUID = Field(default_factory=lambda: uuid.uuid4())

    @property
    def file_format(self):
        return os.path.splitext(self.filename)[-1]


class Currency(BaseModel):
    currency_id: uuid.UUID
    currency: str
