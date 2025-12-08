import base64
from datetime import date
from io import BytesIO
from typing import BinaryIO

import pdf2image
from google import genai
from google.genai import types

from ml_server.domain.parser import Currency, ParserPrediction
from ml_server.infrastructure.schemas.parser import (
    ParsedClientDataSchema,
    ParsedDataSchema,
    ParsedInvoiceDataSchema,
)
from ml_server.services.exceptions import ParserException
from ml_server.services.ports.parser import IParser
from ml_server.utils.logger import get_logger

LOGGER = get_logger()


class TestParser(IParser):
    def parse(self, file: BinaryIO) -> ParserPrediction:
        LOGGER.info("Using TestParser to parse the invoice.")
        # For testing purposes, return a dummy ParserPrediction
        parsed_data_schema = ParsedDataSchema(
            invoice=ParsedInvoiceDataSchema(
                gross_amount=10000,
                vat=20,
                issued_date=date(2023, 10, 1),
                invoice_number="INV-12345",
                invoice_description="Test Invoice",
                currency=Currency.USD,
            ),
            client=ParsedClientDataSchema(
                name="Test Client",
                street_address="123 Client St",
                zipcode="12345",
                city="San Francisco",
                country="USA",
            ),
        )

        return parsed_data_schema.to_prediction(model_name="TestParser")


VLM_PROMPT = """
Analyze this invoice document carefully and extract all relevant information.
Generate a JSON output based on the JSON schema provided below.
If a feature is missing, or if you're not certain, set it to null.
"""


class GeminiParser(IParser):
    def __init__(self, api_key: str, model_name: str) -> None:
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.instructions = """You are an invoice parser.
        Given an image of an invoice, extract the relevant fields and return them in a 
        structured JSON format as specified.
        """

    @staticmethod
    def _process_file(file: BinaryIO) -> str:
        try:
            pdf_bytes = file.read()

            # Convert first page of PDF to image with explicit parameters
            images = pdf2image.convert_from_bytes(pdf_bytes)

            # Convert first page image to base64 string
            with BytesIO() as buffered:
                images[0].save(buffered, format="PNG", optimize=True)
                str_img = base64.b64encode(buffered.getvalue()).decode("utf-8")
            return str_img

        except Exception as e:
            raise ParserException(f"Failed to process PDF file: {str(e)}") from e

    def parse(self, file: BinaryIO) -> ParserPrediction:
        str_img = self._process_file(file)
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[
                types.Part.from_bytes(
                    data=base64.b64decode(str_img),
                    mime_type="image/png",
                ),
                self.instructions,
            ],
            config={
                "response_mime_type": "application/json",
                "response_schema": ParsedDataSchema.model_json_schema(),
            },
        )
        return ParsedDataSchema.model_validate(response.parsed).to_prediction(
            model_name=self.model_name
        )
