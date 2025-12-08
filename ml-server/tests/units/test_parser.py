from datetime import date
from io import BytesIO

import pytest

from ml_server.infrastructure.parser import GeminiParser
from ml_server.infrastructure.schemas.parser import ParsedClientDataSchema, ParsedInvoiceDataSchema
from ml_server.services.exceptions import ParserException

FILE_PATH = "tests/assets/invoice.pdf"


def test_process_file():
    with open(FILE_PATH, "rb") as file:
        img_str = GeminiParser._process_file(file=file)
    assert isinstance(img_str, str)


def test_process_file_invalid():
    invalid_pdf = BytesIO(b"This is not a valid PDF content")
    with pytest.raises(ParserException):
        GeminiParser._process_file(file=invalid_pdf)


def test_parsed_client_schema():
    addr = ParsedClientDataSchema(street_address="123 Main St", city="New York", country="USA")
    assert addr.street_address == "123 Main St"
    assert addr.city == "New York"
    assert addr.country == "USA"
    assert addr.zipcode is None  # Optional field


# Basic test cases for Invoice
def test_parsed_invoice_schema():
    invoice_dict = {
        "gross_amount": 1000,
        "vat": 10,
        "issued_date": "01/01/2023",
        "due_date": "10/01/2023",
        "invoice_number": "INV-001",
        "currency": "USD",
    }
    parsed_invoice_schema = ParsedInvoiceDataSchema.model_validate(invoice_dict)

    assert parsed_invoice_schema.gross_amount == 1000
    assert parsed_invoice_schema.issued_date == date(2023, 1, 1)
    assert parsed_invoice_schema.due_date == date(2023, 1, 10)
    assert parsed_invoice_schema.invoice_number == "INV-001"
    assert parsed_invoice_schema.currency == "USD"


def test_invoice_invalid_amount():
    invoice = ParsedInvoiceDataSchema(gross_amount=-1000)
    assert invoice.gross_amount is None  # Should be filtered out by validator


def test_invoice_invalid_vat():
    invoice = ParsedInvoiceDataSchema(vat=-5)
    assert invoice.vat is None  # Should be filtered out by validator


def test_invoice_wrong_date_format():
    invoice_dict = {
        "issued_date": "01/01/2023",
        "due_date": "10-01-2023",  # Not proper date format
    }
    invoice = ParsedInvoiceDataSchema.model_validate(invoice_dict)
    assert invoice.issued_date == date(2023, 1, 1)
    assert invoice.due_date is None


def test_invoice_due_date_before_issued_date():
    invoice_dict = {
        "issued_date": "01/01/2023",
        "due_date": "01/01/2022",  # Due date before issued date
    }
    invoice = ParsedInvoiceDataSchema.model_validate(invoice_dict)
    assert invoice.issued_date == date(2023, 1, 1)
    assert invoice.due_date is None


def test_invoice_valid_currency():
    invoice_dict = {
        "currency": "EUR",
    }
    invoice = ParsedInvoiceDataSchema.model_validate(invoice_dict)
    assert invoice.currency == "EUR"  # Should be valid currency


def test_invoice_wrong_currency():
    invoice_dict = {
        "currency": "XYZ",
    }
    invoice = ParsedInvoiceDataSchema.model_validate(invoice_dict)
    assert invoice.currency is None  # Should be filtered out by validator
