from abc import ABC, abstractmethod
from typing import BinaryIO

from ml_server.domain.invoice import InvoiceExtraction
from ml_server.services.exceptions import ParserException
from ml_server.utils.logger import get_logger

logger = get_logger()


def _is_pdf(content_type: str) -> bool:
    """Check file format based on MIME type.
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/MIME_types/Common_types
    """
    return content_type == "application/pdf"


class ParserInteface(ABC):
    """Interface/Port for infrastructure adapter."""

    @abstractmethod
    async def parse(self, file: BinaryIO) -> InvoiceExtraction:
        pass


class ParserService:
    @logger.catch
    @staticmethod
    async def parse(file: BinaryIO, content_type: str, parser: ParserInteface) -> InvoiceExtraction:
        logger.info("Starting invoice parsing")
        if not _is_pdf(content_type):
            raise ParserException("File not in PDF format", status_code=422)
        invoice_extraction = await parser.parse(file)
        logger.info("Invoice parsing completed successfully")
        return invoice_extraction
