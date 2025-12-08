from datetime import date
from typing import BinaryIO

import httpx

from invoice_reader.domain.client import ClientData
from invoice_reader.domain.invoice import Currency, InvoiceData
from invoice_reader.infrastructure.schemas.parser import ParsedData
from invoice_reader.services.exceptions import InfrastructureException
from invoice_reader.services.interfaces.parser import IParser
from invoice_reader.settings import get_settings

settings = get_settings()


class TestParser(IParser):
    def parse(self, file: BinaryIO) -> tuple[InvoiceData, ClientData]:
        invoice_data = InvoiceData(
            gross_amount=100.0,
            description="Invoice description",
            vat=20,
            issued_date=date(2023, 1, 1),
            currency=Currency.EUR,
            invoice_number="INV-1000",
        )
        client_data = ClientData(
            client_name="Test Client",
            street_number="123",
            street_address="Test St",
            zipcode="12345",
            city="Test City",
            country="Test Country",
        )
        return invoice_data, client_data


class MLServerParser(IParser):
    def parse(self, file: BinaryIO) -> tuple[InvoiceData, ClientData]:
        """Parse document using the /parser endpoint from the ML server."""
        files = {"upload_file": file}
        response = httpx.post(settings.parser_endpoint, files=files)
        if response.status_code != 200:
            raise InfrastructureException(
                message=f"""Failed to parse the invoice document.\n Error: {response.text}. 
                Response status: {response.status_code}""",
            )
        try:
            parsed_data = ParsedData.model_validate(response.json())
        except Exception as e:
            raise InfrastructureException(
                message="Failed to parse the invoice document. Error: " + str(e),
                status_code=422,
            ) from e
        client_data = parsed_data.client.to_client_data()
        invoice_data = parsed_data.invoice.to_invoice_data()
        return invoice_data, client_data
