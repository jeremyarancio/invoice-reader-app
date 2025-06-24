from abc import ABC, abstractmethod
from typing import BinaryIO
from uuid import UUID

from invoice_reader.infrastructure.togetherai import TogetherAIParser
from invoice_reader.mappers.parser import map_invoice_parsing_to_response
from invoice_reader.repository import ClientRepository, CurrencyRepository
from invoice_reader.schemas.parser import InvoiceExtraction


class InvoiceParser(ABC):
    @abstractmethod
    def parse(self, file: BinaryIO) -> InvoiceExtraction:
        """Parse the invoice image and return structured data."""
        raise NotImplementedError("Subclasses must implement this method.")


class TogetherAIInvoiceParser(InvoiceParser):
    def parse(
        self,
        file: BinaryIO,
        user_id: UUID,
        client_repository: ClientRepository,
        currency_repository: CurrencyRepository,
    ) -> InvoiceExtraction:
        parse = TogetherAIParser()
        invoice_data = parse.parse(file)
        return map_invoice_parsing_to_response(
            invoice_data,
            currency_repository=currency_repository,
            client_repository=client_repository,
            user_id=user_id,
        )
