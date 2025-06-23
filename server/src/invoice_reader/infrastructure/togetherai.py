import json
from datetime import date
from typing import BinaryIO

import together
from pydantic import BaseModel, Field, ValidationError

from invoice_reader import settings
from invoice_reader.app.exceptions import INVALID_EXTRACTED_DATA_EXCEPTION
from invoice_reader.schemas.parser import (
    Address,
    CompanyDataExtraction,
    InvoiceDataExtraction,
    InvoiceExtraction,
)
from invoice_reader.utils.files import convert_pdf_to_base64_image
from invoice_reader.utils.logger import get_logger

LOGGER = get_logger(__name__)


class InvoiceParsingSchema(BaseModel):
    seller_name: str | None = Field(description="Name of the seller", default=None)
    seller_address: str | None = Field(
        description="Address of the seller", default=None
    )
    seller_address_zipcode: str | None = Field(
        description="Zip code of the seller's address", default=None
    )
    seller_address_country: str | None = Field(
        description="Country of the seller's address. Should be the complete name (e.g., France, Germany, etc.)",
        default=None,
    )
    seller_address_city: str | None = Field(
        description="City of the seller's address. Should be the complete name (e.g., Paris, Berlin, etc.)",
        default=None,
    )
    buyer_name: str = Field(description="Name of the buyer")
    buyer_address: str = Field(description="Address of the buyer")
    buyer_address_zipcode: str = Field(description="Zipcode of the buyer's address")
    buyer_address_country: str = Field(
        description="Country of the buyer's address. Should be the complete name (e.g., France, Germany, etc.)"
    )
    buyer_adress_city: str = Field(
        description="City of the buyer's address. Should be the complete name (e.g., Paris, Berlin, etc.)"
    )
    gross_amount: float = Field(description="Total amount of the invoice before tax")
    vat: int = Field(
        description="VAT percentage as positive integer (e.g., 20 for 20%)"
    )
    issued_date: date = Field(
        description="Date when the invoice was issued. Format: DD-MM-YYYY"
    )
    invoice_number: str = Field(description="Unique identifier for the invoice")
    invoice_description: str = Field(
        description="Description of the invoiced service or product."
    )
    currency: str = Field(
        description="Currency of the invoice amount. Should be a valid ISO 4217 currency code (e.g., EUR, USD, GBP).",
    )

    class Config:
        strict = False


def map_invoice_parsing_to_response(
    extraction: InvoiceParsingSchema,
) -> InvoiceExtraction:
    """Maps the extracted data to the InvoiceData model."""
    invoice_extract = InvoiceDataExtraction(
        gross_amount=extraction.gross_amount,
        vat=extraction.vat,
        issued_date=extraction.issued_date,
        invoice_number=extraction.invoice_number,
        invoice_description=extraction.invoice_description,
        currency=extraction.currency,
    )
    client_extract = CompanyDataExtraction(
        name=extraction.buyer_name,
        address=Address(
            street_address=extraction.buyer_address,
            zipcode=extraction.buyer_address_zipcode,
            city=extraction.buyer_adress_city,
            country=extraction.buyer_address_country,
        ),
    )
    seller_extract = CompanyDataExtraction(
        name=extraction.seller_name,
        address=Address(
            street_address=extraction.seller_address,
            zipcode=extraction.seller_address_zipcode,
            city=extraction.seller_address_city,
            country=extraction.seller_address_country,
        ),
    )
    return InvoiceExtraction(
        invoice=invoice_extract, client=client_extract, seller=seller_extract
    )


class TogetherAIParser:
    def __init__(self):
        self.model_name = settings.TOGETHER_MODEL_NAME
        self.client = together.Together()

    def parse(self, file: BinaryIO) -> InvoiceExtraction:
        extract = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an invoice parser. Extract the invoice data from the provided file.",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{convert_pdf_to_base64_image(file)}",
                            },
                        },
                    ],
                },
            ],
            model=self.model_name,
            response_format={
                "type": "json_object",
                "schema": InvoiceParsingSchema.model_json_schema(),
            },
        )
        output = json.loads(extract.choices[0].message.content)
        try:
            invoice_data = InvoiceParsingSchema.model_validate_json(output)
            return map_invoice_parsing_to_response(invoice_data)
        except ValidationError as e:
            LOGGER.error(
                "Invalid data extracted from the invoice. Data: %s",
                output,
            )
            raise INVALID_EXTRACTED_DATA_EXCEPTION from e
