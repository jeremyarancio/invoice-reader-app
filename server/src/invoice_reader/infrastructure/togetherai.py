import json
from datetime import date, datetime
from typing import BinaryIO

import together
from pydantic import BaseModel, Field, ValidationError, field_validator

from invoice_reader import settings
from invoice_reader.app.exceptions import INVALID_EXTRACTED_DATA_EXCEPTION
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
        description="Country of the buyer's address. Should be the complete name (e.g., France, Germany, etc.)",
    )
    buyer_address_city: str = Field(
        description="City of the buyer's address. Should be the complete name (e.g., Paris, Berlin, etc.)",
    )
    gross_amount: float = Field(description="Total amount of the invoice before tax")
    vat: int = Field(
        description="VAT percentage as positive integer (e.g., 20 for 20%)",
    )
    # Default to None to allow for optional fields
    issued_date: date | None = Field(
        description="Date when the invoice was issued. Format: DD-MM-YYYY", default=None
    )
    invoice_number: str = Field(description="Unique identifier for the invoice")
    invoice_description: str = Field(
        description="Description of the invoiced service or product."
    )
    currency: str = Field(
        description="Currency of the invoice amount. Should be a valid ISO 4217 currency code (e.g., EUR, USD, GBP).",
    )

    @field_validator("issued_date", mode="before")
    @classmethod
    def validate_date(cls, value: str) -> date | None:
        """We return None if the date is not valid instead of validation error."""
        try:
            return datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:
            return None


class TogetherAIParser:
    def __init__(self):
        self.model_name = settings.TOGETHER_MODEL_NAME
        self.client = together.Together()

    def parse(self, file: BinaryIO) -> InvoiceParsingSchema:
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
        try:
            output = json.loads(extract.choices[0].message.content)
            invoice_data = InvoiceParsingSchema.model_validate(output)
            return invoice_data
        except json.JSONDecodeError as e:
            LOGGER.error(
                "Failed to decode JSON response from the model.\n Error: %s\n Response: %s",
                e,
                extract.choices[0].message.content,
            )
            raise INVALID_EXTRACTED_DATA_EXCEPTION from e
        except ValidationError as e:
            LOGGER.error(
                "Invalid data extracted from the invoice.\n Error: %s\n Data: %s",
                e,
                output,
            )
            raise INVALID_EXTRACTED_DATA_EXCEPTION from e


if __name__ == "__main__":
    # Example usage
    FILE_PATH = "assets/invoice.pdf"
    with open(FILE_PATH, "rb") as file:
        parser = TogetherAIParser()
        try:
            invoice_extraction = parser.parse(file)
            print(invoice_extraction)
        except Exception as e:
            LOGGER.error("Failed to parse invoice: %s", e)
