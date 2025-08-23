import os
import uuid

from pydantic import BaseModel, Field

from .clients import *
from .invoices import *
from .users import *


class AuthToken(BaseModel):
    access_token: str
    token_type: str


class Currency(BaseModel):
    currency_id: uuid.UUID
    currency: str
