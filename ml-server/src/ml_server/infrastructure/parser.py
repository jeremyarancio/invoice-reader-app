import base64
from datetime import date
from io import BytesIO
from typing import BinaryIO

import pdf2image
from openai import AsyncOpenAI
from pydantic import ValidationError

from ml_server.domain.invoice import (
    Address,
    Client,
    Invoice,
    InvoiceExtraction,
    Seller,
)
from ml_server.services.exceptions import ParserException
from ml_server.services.parser import ParserInteface
from ml_server.settings import settings
from ml_server.utils.logger import get_logger

LOGGER = get_logger()


class TestParser(ParserInteface):
    async def parse(self, file: BinaryIO) -> InvoiceExtraction:
        return InvoiceExtraction(
            invoice=Invoice(
                gross_amount=10000,
                vat=20,
                issued_date=date(2023, 10, 1),
                invoice_number="INV-12345",
                invoice_description="Test Invoice",
                currency="USD",
            ),
            client=Client(
                name="Test Client",
                address=Address(
                    street_address="123 Client St",
                    zipcode="12345",
                    city="San Francisco",
                    country="USA",
                ),
            ),
            seller=Seller(
                name="Test Seller",
                address=Address(
                    street_address="18 Rue de Rivoli",
                    zipcode="67890",
                    city="Paris",
                    country="FRA",
                ),
            ),
        )


VLM_PROMPT = """
Analyze this invoice document carefully and extract all relevant information.
Generate a JSON output based on the JSON schema provided below.
If a feature is missing, or if you're not certain, set it to null.
"""


class vLLMParser(ParserInteface):
    """Invoice Parser using Nanonets OCR: https://huggingface.co/nanonets/Nanonets-OCR-s,
    deployed on Cloud Run with vLLM.
    """

    @staticmethod
    async def _process_file(file: BinaryIO) -> str:
        try:
            pdf_bytes = file.read()

            # Convert first page of PDF to image with explicit parameters
            images = pdf2image.convert_from_bytes(pdf_bytes)

            # Convert first page image to base64 string
            with BytesIO() as buffered:
                images[0].save(buffered, format="PNG", optimize=True)
                img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            return img_str

        except Exception as e:
            raise ParserException(f"Failed to process PDF file: {str(e)}") from e

    async def parse(self, file: BinaryIO) -> InvoiceExtraction:
        """Using the deployed VLM, parse the document and return the extracted information."""
        img_str = await self._process_file(file=file)

        client = AsyncOpenAI(
            base_url=settings.parser_api_url + "/v1",
            api_key=settings.parser_api_key,
        )

        response = await client.chat.completions.parse(
            model=settings.model_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"{VLM_PROMPT}"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{img_str}",
                            },
                        },
                    ],
                }
            ],
            response_format=InvoiceExtraction,
        )

        LOGGER.info("LLM response: {}", response.to_json(indent=2))
        LOGGER.info(
            "Token usage : {}",
            response.usage.to_json(indent=2) if response.usage else "No usage data",
        )

        output = response.choices[0].message
        if output.refusal:
            raise ParserException(
                f"Error during image processing.\nOutput:\n{output.to_json(indent=2)}"
            )
        else:
            LOGGER.info("LLM output: {}", output.content)
            try:
                invoice_extraction = InvoiceExtraction.model_validate_json(output.content)
            except ValidationError as e:
                raise ParserException(f"Failed to extract JSON from LLM output: {str(e)}") from e

        return invoice_extraction


if __name__ == "__main__":
    import asyncio
    from pathlib import Path

    parser = vLLMParser()
    with open(Path.home() / "invoice.pdf", "rb") as file:
        asyncio.run(parser.parse(file=file))
