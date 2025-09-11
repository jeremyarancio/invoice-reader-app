from datetime import date

import pytest

from invoice_reader.models import ClientModel, CurrencyModel
from invoice_reader.schemas.invoices import InvoiceBase, InvoiceCreate

TOTAL_N = 3


@pytest.fixture
def new_invoice():
    return InvoiceBase(
        invoiced_date=date(2024, 11, 18),
        invoice_number="14SQ456",
        gross_amount=10000,
        vat=20,
        description="Test invoice",
    )


@pytest.fixture
def existing_invoice() -> InvoiceBase:
    return InvoiceBase(
        invoiced_date=date(2024, 12, 20),
        invoice_number="14SQ456",
        gross_amount=10000,
        vat=20,
        description="Test invoice",
        paid_date=None,
    )


@pytest.fixture
def existing_invoices() -> list[InvoiceBase]:
    return [
        InvoiceBase(
            invoiced_date=date(2024, 11, 18),
            invoice_number=f"number-{i}",
            gross_amount=10000,
            vat=20,
            description=f"Test invoice {i}",
            paid_date=None,
        )
        for i in range(TOTAL_N)
    ]


@pytest.fixture
def new_invoice_create(
    test_existing_client: ClientModel,
    new_invoice: InvoiceBase,
    test_existing_currency: CurrencyModel,
) -> InvoiceCreate:
    return InvoiceCreate(
        client_id=test_existing_client.client_id,
        currency_id=test_existing_currency.id,
        invoice=new_invoice,
    )


@pytest.fixture
def existing_invoice_create(
    test_existing_client: ClientModel,
    existing_invoice: InvoiceBase,
    test_existing_currency: CurrencyModel,
) -> InvoiceCreate:
    return InvoiceCreate(
        client_id=test_existing_client.client_id,
        currency_id=test_existing_currency.id,
        invoice=existing_invoice,
    )
