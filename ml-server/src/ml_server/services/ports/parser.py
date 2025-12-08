from abc import ABC, abstractmethod
from typing import BinaryIO

from ml_server.domain.parser import ParserPrediction


class IParser(ABC):
    """Interface/Port for infrastructure adapter."""

    @abstractmethod
    def parse(self, file: BinaryIO) -> ParserPrediction:
        pass
