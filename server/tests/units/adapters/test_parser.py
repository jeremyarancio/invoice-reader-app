import io
from datetime import date
from typing import BinaryIO
from unittest.mock import MagicMock, patch

import pytest

from invoice_reader.domain.invoice import Currency
from invoice_reader.domain.parser import ParsedClientData, ParsedInvoiceData, ParserExtraction
from invoice_reader.infrastructure.parser import MLServerParser
from invoice_reader.services.exceptions import InfrastructureException


@pytest.fixture
def parser():
    return MLServerParser()


@pytest.fixture
def mock_parsed_data() -> ParserExtraction:
    return ParserExtraction(
        invoice=ParsedInvoiceData(
            currency=Currency.USD,
            gross_amount=1500.75,
            invoice_number="12345",
            issued_date=date(2023, 10, 1),
            invoice_description="Invoice",
            vat=20,
        ),
        client=ParsedClientData(
            client_name="Test Client",
            street_address="123 Test St",
            zipcode="12345",
            city="Paris",
            country="France",
        ),
    )


@pytest.fixture
def mock_uncomplete_parsed_data() -> ParserExtraction:
    return ParserExtraction(
        invoice=ParsedInvoiceData(
            currency=None,
            invoice_number="12345",
            issued_date=date(2023, 10, 1),
            invoice_description="Invoice",
            gross_amount=None,
            vat=None,
        ),
        client=ParsedClientData(
            client_name=None,
            street_address=None,
            zipcode=None,
            city=None,
            country="France",
        ),
    )


@pytest.fixture
def file() -> BinaryIO:
    return io.BytesIO(b"dummy data")


def test_parse_success(parser: MLServerParser, file: BinaryIO, mock_parsed_data: ParserExtraction):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_parsed_data.model_dump()
    with patch("httpx.post", return_value=mock_response):
        result = parser.parse(file)
        assert result == mock_parsed_data


def test_parse_http_error(parser: MLServerParser, file: BinaryIO):
    mock_response = MagicMock()
    mock_response.status_code = 500
    with patch("httpx.post", return_value=mock_response), pytest.raises(InfrastructureException):
        parser.parse(file)


def test_parse_validation_error(parser: MLServerParser, file: BinaryIO):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"invoice_number": "12345"}
    with (
        patch("httpx.post", return_value=mock_response),
        pytest.raises(InfrastructureException) as exc,
    ):
        parser.parse(file)
        assert exc.value.status_code == 422


def test_parse_success_with_uncomplete_data(
    parser: MLServerParser, file: BinaryIO, mock_uncomplete_parsed_data: ParserExtraction
):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_uncomplete_parsed_data.model_dump()
    with patch("httpx.post", return_value=mock_response):
        result = parser.parse(file)
        assert result == mock_uncomplete_parsed_data
