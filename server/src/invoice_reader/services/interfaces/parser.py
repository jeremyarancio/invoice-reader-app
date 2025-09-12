from abc import ABC, abstractmethod
from typing import BinaryIO

from invoice_reader.domain.parser import ParserExtraction


class IParser(ABC):
    @abstractmethod
    def parse(self, file: BinaryIO) -> ParserExtraction:
        raise NotImplementedError
