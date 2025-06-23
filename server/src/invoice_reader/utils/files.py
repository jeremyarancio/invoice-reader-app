import base64
from typing import BinaryIO

from pdf2image import convert_from_bytes
from PIL.Image import Image


def _encode_image(image: Image) -> str:
    return base64.b64encode(image.tobytes()).decode("utf-8")


def _convert_pdf_to_image(pdf_file: BinaryIO) -> Image:
    images = convert_from_bytes(pdf_file.read())
    return images[0]


def convert_pdf_to_base64_image(pdf_file: BinaryIO) -> str:
    image = _convert_pdf_to_image(pdf_file)
    return _encode_image(image)
