from datetime import datetime
import io
from PIL import Image

from google import genai
from google.genai import types
import tqdm

from parser.domain.parse import Prediction, ParsedData
from parser.infrastructure.schemas.parser import ParsedInvoice
from parser.service.ports.parser import IParser


class MockParser(IParser):
    def parse(self, images: list[Image.Image]) -> list[Prediction]:
        return [
            Prediction(
                model_name="mock",
                data=ParsedData(
                    currency="USD",
                    gross_amount=100.50,
                    vat=20.10,
                    issued_date=datetime(2023, 1, 15),
                    invoice_number="INV-001",
                    client_name="John Doe",
                    client_street_address_number="123",
                    client_street_address="Main Street",
                    client_city="New York",
                    client_zipcode="10001",
                    client_country="USA",
                ),
            )
        ] * len(images)


class GeminiParser(IParser):
    def __init__(self, api_key: str, model_name: str) -> None:
        self.api_key = api_key
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = model_name
        self.instructions = """You are an invoice parser.
        Given an image of an invoice, extract the relevant fields and return them in a structured JSON format as specified.
        """

    def parse(self, images: list[Image.Image]) -> list[Prediction]:
        predictions = []
        for image in tqdm.tqdm(
            images,
            desc="Parsing images with Gemini",
            total=len(images),
        ):
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            img_bytes = buf.getvalue()

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[
                    types.Part.from_bytes(
                        data=img_bytes,
                        mime_type="image/png",
                    ),
                    self.instructions,
                ],
                config={
                    "response_mime_type": "application/json",
                    "response_schema": ParsedInvoice.model_json_schema(),
                },
            )
            predictions.append(
                ParsedInvoice.model_validate(response.parsed).to_prediction(
                    model_name=self.model_name
                )
            )
        return predictions
