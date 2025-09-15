from datetime import date
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from invoice_reader.domain.invoice import Invoice, InvoiceBase, Currency, File, InvoiceUpdate
from invoice_reader.domain.client import Client
from invoice_reader.domain.user import User
from invoice_reader.infrastructure.repositories.invoice import InMemoryInvoiceRepository
from invoice_reader.interfaces.schemas.invoice import InvoiceCreate


TOTAL_N = 3


@pytest.fixture
def filepath() -> Path:
    return Path("tests/assets/paper.pdf")


@pytest.fixture
def file(filepath: Path, user: User, invoice_id: UUID) -> File:
    with open(filepath, "rb") as f:
        return File(
            filename=filepath.name,
            file=f.read(),
            storage_path=f"inmemory://bucket/{user.id_}/{invoice_id}{filepath.suffix}",
        )


@pytest.fixture
def upload_files(file: File):
    files = {"upload_file": (file.filename, file.file, "application/pdf")}
    yield files


@pytest.fixture
def invoice_base() -> InvoiceBase:
    return InvoiceBase(
        invoice_number="14SQ456",
        gross_amount=10000,
        vat=20,
        description="Test invoice",
        issued_date=date(2024, 11, 18),
        paid_date=None,
        currency=Currency.EUR,
    )


@pytest.fixture
def invoice_id() -> UUID:
    return uuid4()


@pytest.fixture
def invoice(
    invoice_id: UUID, invoice_base: InvoiceBase, client: Client, user: User, file: File
) -> Invoice:
    # TODO: remove this **model_dump() logic: futur bugs
    return Invoice(
        id_=invoice_id,
        client_id=client.id_,
        user_id=user.id_,
        storage_path=file.storage_path,
        **invoice_base.model_dump(),
    )


@pytest.fixture
def existing_invoice(invoice: Invoice) -> Invoice:
    InMemoryInvoiceRepository().add(invoice=invoice)
    return invoice


@pytest.fixture
def invoice_create(invoice_base: InvoiceBase, client: Client) -> InvoiceCreate:
    return InvoiceCreate(
        client_id=client.id_,
        invoice=invoice_base,
    )


@pytest.fixture
def invoice_update(client: Client, invoice_base: InvoiceBase) -> InvoiceUpdate:
    invoice_base.gross_amount = 20000
    invoice_base.vat = 10
    return InvoiceUpdate(client_id=client.id_, **invoice_base.model_dump())
