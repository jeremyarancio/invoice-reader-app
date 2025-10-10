from datetime import date

from invoice_reader.domain.client import Client
from invoice_reader.domain.invoice import Amount, Currency, Invoice, InvoiceData
from invoice_reader.domain.user import User


def test_total_revenue_with_no_invoices(client: Client):
    """Test that total_revenue returns None when there are no invoices."""
    assert client.total_revenue.base_amount == 0


def test_total_revenue_with_multiple_invoices(client_with_invoices: Client):
    """Test that total_revenue sums multiple invoice amounts correctly."""
    total_revenue = client_with_invoices.total_revenue
    assert total_revenue is not None
    assert (
        total_revenue.base_currency == client_with_invoices.invoices[0].gross_amount.base_currency
    )
    assert total_revenue.currency_amounts[Currency.EUR] == 10000 * 3  # 3 invoices of 10000 EUR each
    assert total_revenue.currency_amounts[Currency.USD] == 11000 * 3


def test_total_revenue_with_mismatched_currencies(client_with_invoices: Client, user: User):
    amount = Amount(
        currency_amounts={
            Currency.EUR: 100.0,
            Currency.USD: 110.0,
        },
        base_currency=Currency.EUR,
    )

    invoice = Invoice(
        client_id=client_with_invoices.id_,
        user_id=user.id_,
        storage_path="test/path1",
        data=InvoiceData(
            invoice_number="INV001",
            vat=20,
            description="Test invoice 1",
            issued_date=date(2024, 1, 1),
        ),
        gross_amount=amount,
    )
    client_with_new_invoice = client_with_invoices.model_copy(deep=True)
    client_with_new_invoice.invoices.append(invoice)

    assert client_with_new_invoice.total_revenue is not None
    assert client_with_new_invoice.total_revenue.currency_amounts == {}
