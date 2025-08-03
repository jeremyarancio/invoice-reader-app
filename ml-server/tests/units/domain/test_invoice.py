from datetime import date

from ml_server.domain.invoice import Address, Invoice


# Basic test cases for Address
def test_address_creation():
    addr = Address(street_address="123 Main St", city="New York", country="USA")
    assert addr.street_address == "123 Main St"
    assert addr.city == "New York"
    assert addr.country == "USA"
    assert addr.zipcode is None  # Optional field


# Basic test cases for Invoice
def test_invoice():
    invoice_dict = {
        "gross_amount": 1000,
        "vat": 10,
        "issued_date": "01/01/2023",
        "due_date": "10/01/2023",
        "invoice_number": "INV-001",
        "currency": "USD",
    }
    invoice = Invoice.model_validate(invoice_dict)

    assert invoice.gross_amount == 1000
    assert invoice.issued_date == date(2023, 1, 1)
    assert invoice.due_date == date(2023, 1, 10)
    assert invoice.invoice_number == "INV-001"
    assert invoice.currency == "USD"


def test_invoice_invalid_amount():
    invoice = Invoice(gross_amount=-1000)
    assert invoice.gross_amount is None  # Should be filtered out by validator


def test_invoice_invalid_vat():
    invoice = Invoice(vat=-5)
    assert invoice.vat is None  # Should be filtered out by validator


def test_invoice_wrong_date_format():
    invoice_dict = {
        "issued_date": "01/01/2023",
        "due_date": "10-01-2023",  # Not proper date format
    }
    invoice = Invoice.model_validate(invoice_dict)
    assert invoice.issued_date == date(2023, 1, 1)
    assert invoice.due_date is None


def test_invoice_due_date_before_issued_date():
    invoice_dict = {
        "issued_date": "01/01/2023",
        "due_date": "01/01/2022",  # Due date before issued date
    }
    invoice = Invoice.model_validate(invoice_dict)
    assert invoice.issued_date == date(2023, 1, 1)
    assert invoice.due_date is None


def test_invoice_valid_currency():
    invoice_dict = {
        "currency": "EUR",
    }
    invoice = Invoice.model_validate(invoice_dict)
    assert invoice.currency == "EUR"  # Should be valid currency


def test_invoice_wrong_currency():
    invoice_dict = {
        "currency": "XYZ",
    }
    invoice = Invoice.model_validate(invoice_dict)
    assert invoice.currency is None  # Should be filtered out by validator
