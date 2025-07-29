import base64
from datetime import date
from io import BytesIO
from typing import BinaryIO

from PIL.Image import Image
import pdf2image
import openai

from ml_server.settings import settings
from ml_server.services.parser import ParserInteface
from ml_server.services.exceptions import ParserException
from ml_server.domain.invoice import (
    InvoiceExtraction,
    Invoice,
    Client,
    Seller,
    Currency,
    Address,
)


class TestParser(ParserInteface):
    def parse(self, file: BytesIO) -> InvoiceExtraction:
        return InvoiceExtraction(
            invoice=Invoice(
                gross_amount=10000,
                vat=20,
                issued_date=date(2023, 10, 1),
                invoice_number="INV-12345",
                invoice_description="Test Invoice",
                currency=Currency.USD,
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


class vLLMParser(ParserInteface):
    """Invoice Parser using Nanonets OCR: https://huggingface.co/nanonets/Nanonets-OCR-s, deployed on Cloud Run with vLLM."""

    @staticmethod
    def _process_file(file: BinaryIO) -> str:
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
            raise ParserException(f"Failed to process PDF file: {str(e)}")

    def parse(self, file: BinaryIO) -> InvoiceExtraction:
        img_str = self._process_file(file=file)

        # messages = [
        #     {"role": "system", "content": "You are a helpful assistant."},
        #     {
        #         "role": "user",
        #         "content": [
        #             {"type": "image_url", "url": f"data:image/png;base64,{img_str}"},
        #             {
        #                 "type": "text",
        #                 "text": self.prompt,
        #             },
        #         ],
        #     },
        # ]
        # text = self.processor.apply_chat_template(
        #     messages, tokenize=False, add_generation_prompt=True
        # )
        # inputs = self.processor(
        #     text=[text], images=[image], padding=True, return_tensors="pt"
        # )
        # output_ids = self.model.generate(
        #     **inputs, max_new_tokens=max_new_tokens, do_sample=False
        # )
        # output_text = self.processor.batch_decode(
        #     output_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True
        # )
        # return output_text[0]
