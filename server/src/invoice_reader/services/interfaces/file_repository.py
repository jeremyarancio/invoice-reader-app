from abc import ABC, abstractmethod
from typing import BinaryIO


class IFileRepository(ABC):
    @abstractmethod
    def store(self, file: BinaryIO) -> None:
        pass

    @abstractmethod
    def delete(self, file_path: str) -> None:
        pass

    @abstractmethod
    def get_url(self, file_path: str) -> str:
        pass
