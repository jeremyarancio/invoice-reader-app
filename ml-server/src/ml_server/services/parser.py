from abc import ABC, abstractmethod
from typing import BinaryIO

from ml_server.services.exceptions import ParserException
from ml_server.domain.invoice import InvoiceExtraction
from ml_server.utils.logger import get_logger


logger = get_logger()


class ParserInteface(ABC):
    @abstractmethod
    async def parse(self, file: BinaryIO) -> InvoiceExtraction:
        pass


class ParserService:
    async def parse(self, file: BinaryIO, parser: ParserInteface) -> InvoiceExtraction:
        try:
            logger.info("Starting invoice parsing")
            invoice_extraction = await parser.parse(file)
            logger.info("Invoice parsing completed successfully")
            return invoice_extraction
        except ParserException:
            raise
