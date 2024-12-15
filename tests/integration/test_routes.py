import json
from unittest.mock import Mock

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from invoice_reader import (
    models,  # noqa: F401
)
from invoice_reader.models import ClientModel, InvoiceModel
from invoice_reader.schemas import (
    AuthToken,
    Client,
    FileData,
    Invoice,
    InvoiceCreate,
    InvoiceResponse,
    PagedClientResponse,
    PagedInvoiceResponse,
    User,
)


