from datetime import date
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from invoice_reader.domain.client import Client
from invoice_reader.domain.invoice import Currency, File, Invoice, InvoiceData
from invoice_reader.domain.user import User
from invoice_reader.infrastructure.repositories.file import InMemoryFileRepository
from invoice_reader.infrastructure.repositories.invoice import InMemoryInvoiceRepository
from invoice_reader.interfaces.schemas.invoice import InvoiceCreate, InvoiceUpdate


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
def invoice_data() -> InvoiceData:
    return InvoiceData(
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
    invoice_id: UUID, invoice_data: InvoiceData, client: Client, user: User, file: File
) -> Invoice:
    return Invoice(
        id_=invoice_id,
        client_id=client.id_,
        user_id=user.id_,
        storage_path=file.storage_path,
        data=invoice_data,
    )


@pytest.fixture
def existing_invoice(invoice: Invoice) -> Invoice:
    InMemoryInvoiceRepository().add(invoice=invoice)
    return invoice


@pytest.fixture
def invoice_create(invoice_data: InvoiceData, client: Client) -> InvoiceCreate:
    return InvoiceCreate(
        client_id=client.id_,
        data=invoice_data,
    )


@pytest.fixture
def invoice_update(client: Client, invoice_data: InvoiceData) -> InvoiceUpdate:
    return InvoiceUpdate(
        client_id=client.id_,
        data=invoice_data.model_copy(
            update={
                "gross_amount": 20000,
                "vat": 10,
                "description": "Updated test invoice",
                "issued_date": date(2024, 11, 20),
            }
        ),
    )


@pytest.fixture
def existing_file(file: File) -> File:
    InMemoryFileRepository().store(file=file)
    return file
