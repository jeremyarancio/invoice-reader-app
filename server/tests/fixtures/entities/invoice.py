from datetime import date
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from invoice_reader.domain.client import Client
from invoice_reader.domain.invoice import Amount, Currency, File, Invoice, InvoiceData
from invoice_reader.domain.user import User
from invoice_reader.infrastructure.repositories.file import InMemoryFileRepository
from invoice_reader.infrastructure.repositories.invoice import InMemoryInvoiceRepository
from invoice_reader.interfaces.schemas.invoice import (
    InvoiceCreate,
    InvoiceInterfaceData,
    InvoiceUpdate,
)


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
def gross_amount() -> Amount:
    """Gross amount with conversions matching TestExchangeRatesService rates.

    Base: EUR 10,000
    Using rates: EUR=1.0, USD=1.1, GBP=0.9, CZK=24.0
    Results in: EUR 10,000, USD 11,000, GBP 9,000, CZK 240,000
    """
    return Amount(
        currency_amounts={
            Currency.EUR: 10000.0,
            Currency.USD: 11000.0,  # 10,000 * 1.1
            Currency.GBP: 9000.0,  # 10,000 * 0.9
            Currency.CZK: 240000.0,  # 10,000 * 24.0
        },
        base_currency=Currency.EUR,
    )


@pytest.fixture
def invoice_data() -> InvoiceData:
    return InvoiceData(
        invoice_number="14SQ456",
        vat=20,
        description="Test invoice",
        issued_date=date(2024, 11, 18),
        paid_date=None,
    )


@pytest.fixture
def invoice_id() -> UUID:
    return uuid4()


@pytest.fixture
def invoice(
    invoice_id: UUID,
    invoice_data: InvoiceData,
    gross_amount: Amount,
    client: Client,
    user: User,
    file: File,
) -> Invoice:
    return Invoice(
        id_=invoice_id,
        client_id=client.id_,
        user_id=user.id_,
        storage_path=file.storage_path,
        data=invoice_data,
        gross_amount=gross_amount,
    )


@pytest.fixture
def existing_invoice(invoice: Invoice) -> Invoice:
    InMemoryInvoiceRepository().add(invoice=invoice)
    return invoice


@pytest.fixture
def invoice_interface_data(invoice_data: InvoiceData, gross_amount: Amount) -> InvoiceInterfaceData:
    return InvoiceInterfaceData(
        invoice_number=invoice_data.invoice_number,
        gross_amount=gross_amount.base_amount,
        currency=gross_amount.base_currency,
        vat=invoice_data.vat,
        description=invoice_data.description,
        issued_date=invoice_data.issued_date,
        paid_date=invoice_data.paid_date,
    )


@pytest.fixture
def invoice_create(invoice_interface_data: InvoiceInterfaceData, client: Client) -> InvoiceCreate:
    return InvoiceCreate(
        client_id=client.id_,
        data=invoice_interface_data,
    )


@pytest.fixture
def invoice_update(client: Client, invoice_interface_data: InvoiceInterfaceData) -> InvoiceUpdate:
    return InvoiceUpdate(
        client_id=client.id_,
        data=invoice_interface_data.model_copy(
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
