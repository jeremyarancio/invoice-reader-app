from abc import ABC, abstractmethod
from typing import BinaryIO

from invoice_reader.domain.client import ClientData
from invoice_reader.domain.invoice import InvoiceData


class IParser(ABC):
    @abstractmethod
    def parse(self, file: BinaryIO) -> tuple[InvoiceData, ClientData]:
        raise NotImplementedError
