from io import BytesIO

import pytest

from ml_server.infrastructure.parser import vLLMParser
from ml_server.services.exceptions import ParserException

FILE_PATH = "tests/assets/invoice.pdf"


@pytest.mark.asyncio
async def test_process_file():
    with open(FILE_PATH, "rb") as file:
        img_str = await vLLMParser._process_file(file=file)
    assert isinstance(img_str, str)


@pytest.mark.asyncio
async def test_process_file_invalid():
    invalid_pdf = BytesIO(b"This is not a valid PDF content")
    with pytest.raises(ParserException):
        await vLLMParser._process_file(file=invalid_pdf)
