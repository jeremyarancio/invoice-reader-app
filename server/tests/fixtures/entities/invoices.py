from datetime import date

import pytest

from invoice_reader.models import ClientModel
from invoice_reader.schemas import invoice_schema

TOTAL_N = 3


@pytest.fixture
def new_invoice():
    return invoice_schema.Invoice(
        invoiced_date=date(2024, 11, 18),
        invoice_number="14SQ456",
        amount_excluding_tax=10000,
        currency="€",
        vat=20,
        is_paid=True,
    )


@pytest.fixture
def existing_invoice() -> invoice_schema.InvoiceBase:
    return invoice_schema.InvoiceBase(
        invoiced_date=date(2024, 12, 20),
        invoice_number="14SQ456",
        amount_excluding_tax=10000,
        currency="€",
        vat=20,
        is_paid=False,
    )


@pytest.fixture
def existing_invoices() -> list[invoice_schema.InvoiceBase]:
    return [
        invoice_schema.InvoiceBase(
            invoiced_date=date(2024, 11, 18),
            invoice_number=f"number-{i}",
            amount_excluding_tax=10000,
            currency="€",
            vat=20,
            is_paid=True,
        )
        for i in range(TOTAL_N)
    ]


@pytest.fixture
def new_invoice_create(
    test_existing_client: ClientModel, new_invoice: invoice_schema.InvoiceBase
) -> invoice_schema.InvoiceCreate:
    return invoice_schema.InvoiceCreate(
        client_id=test_existing_client.client_id, invoice=new_invoice
    )


@pytest.fixture
def existing_invoice_create(
    test_existing_client: ClientModel, existing_invoice: invoice_schema.InvoiceBase
) -> invoice_schema.InvoiceCreate:
    return invoice_schema.InvoiceCreate(
        client_id=test_existing_client.client_id, invoice=existing_invoice
    )
