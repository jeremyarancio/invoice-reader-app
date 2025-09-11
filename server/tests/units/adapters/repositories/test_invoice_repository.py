from datetime import date

import pytest
from sqlmodel import Session

from invoice_reader.domain.client import ClientID
from invoice_reader.domain.invoice import Currency, Invoice
from invoice_reader.domain.user import UserID
from invoice_reader.infrastructure.repositories.invoice import SQLModelInvoiceRepository


@pytest.fixture
def repository(session: Session) -> SQLModelInvoiceRepository:
    return SQLModelInvoiceRepository(session)


@pytest.fixture
def invoice() -> Invoice:
    return Invoice(
        user_id=UserID.create(),
        client_id=ClientID.create(),
        currency=Currency.USD,
        invoice_number="INV-001",
        gross_amount=100.0,
        vat=20,
        description="Test invoice",
        issued_date=date(2025, 9, 10),
        paid_date=date(2025, 9, 11),
        storage_path="/tmp/inv_1.pdf",
    )


def test_add_and_get_invoice(repository: SQLModelInvoiceRepository, invoice: Invoice):
    repository.add(invoice)
    result = repository.get(invoice.id_)
    assert result is not None
    assert result.invoice_number == invoice.invoice_number
    assert result.user_id == invoice.user_id


def test_get_all_invoices(repository: SQLModelInvoiceRepository, invoice: Invoice):
    repository.add(invoice)
    invoices = repository.get_all(invoice.user_id)
    assert len(invoices) == 1
    for invoice in invoices:
        assert invoice.invoice_number == invoice.invoice_number


def test_get_by_invoice_number(repository: SQLModelInvoiceRepository, invoice: Invoice):
    repository.add(invoice)
    result = repository.get_by_invoice_number(invoice.invoice_number, invoice.user_id)
    assert result is not None
    assert result.id_ == invoice.id_


def test_update_invoice(repository: SQLModelInvoiceRepository, invoice: Invoice):
    repository.add(invoice)
    invoice.description = "Updated description"
    repository.update(invoice)
    updated = repository.get(invoice.id_)
    assert updated is not None
    assert updated.description == "Updated description"


def test_delete_invoice(repository: SQLModelInvoiceRepository, invoice: Invoice):
    repository.add(invoice)
    repository.delete(invoice.id_)
    result = repository.get(invoice.id_)
    assert result is None
