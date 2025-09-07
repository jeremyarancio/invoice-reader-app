
import base64
from io import BytesIO
from typing import BinaryIO

import pdf2image
from PIL.Image import Image


def _encode_image(pil_image: Image) -> str:
    """Convert PIL Image to base64 string"""
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def _convert_pdf_to_image(pdf_file: BinaryIO) -> Image:
    images = pdf2image.convert_from_bytes(pdf_file.read())
    return images[0]


def convert_pdf_to_base64_image(pdf_file: BinaryIO) -> str:
    image = _convert_pdf_to_image(pdf_file)
    return _encode_image(image)
