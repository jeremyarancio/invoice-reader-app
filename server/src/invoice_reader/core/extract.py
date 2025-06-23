from abc import ABC, abstractmethod
from typing import BinaryIO

from invoice_reader.infrastructure.togetherai import TogetherAIParser
from invoice_reader.schemas.parser import InvoiceExtraction


class InvoiceParser(ABC):
    @abstractmethod
    def parse(self, file: BinaryIO) -> InvoiceExtraction:
        """Parse the invoice image and return structured data."""
        raise NotImplementedError("Subclasses must implement this method.")


class TogetherAIInvoiceParser(InvoiceParser):
    def parse(self, file: BinaryIO) -> InvoiceExtraction:
        parse = TogetherAIParser()
        invoice_data = parse.parse(file)
        return invoice_data
