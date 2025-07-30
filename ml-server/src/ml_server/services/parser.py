from abc import ABC, abstractmethod
from typing import BinaryIO

from ml_server.domain.invoice import InvoiceExtraction
from ml_server.services.exceptions import ParserException
from ml_server.utils.logger import get_logger

LOGGER = get_logger()


class ParserInteface(ABC):
    """Interface/Port for infrastructure adapter."""

    @abstractmethod
    async def parse(self, file: BinaryIO) -> InvoiceExtraction:
        pass


class ParserService:
    @staticmethod
    async def parse(file: BinaryIO, parser: ParserInteface) -> InvoiceExtraction:
        LOGGER.info("Starting invoice parsing")
        invoice_extraction = await parser.parse(file)
        LOGGER.info("Invoice parsing completed successfully")
        return invoice_extraction
