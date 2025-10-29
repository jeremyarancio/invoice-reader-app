from datetime import datetime
from PIL.Image import Image

from google import genai
from google.genai import types

from parser.domain.prediction import Prediction
from parser.service.ports.parser import IParser
from parser.settings import get_settings


settings = get_settings()


class MockParser(IParser):
    def parse(self, images: list[Image]) -> list[Prediction]:
        return [
            Prediction(
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
            )
        ] * len(images)


class Gemini2_5FlashParser(IParser):
    def __init__(self) -> None:
        self.instructions = """You are an invoice parser.
        Given an image of an invoice, extract the relevant fields and return them in a structured JSON format as specified.
        """

    def parse(self, images: list[Image]) -> list[Prediction]:
        client = genai.Client(api_key=settings.gemini_api_key)
        for image in images:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Part.from_bytes(
                        data=image.tobytes(),
                        mime_type="image/jpeg",
                    ),
                    self.instructions,
                ],
                config={
                    "response_mime_type": "application/json",
                    "response_schema": Prediction,
                },
            )
        return response.parsed  # type: ignore
