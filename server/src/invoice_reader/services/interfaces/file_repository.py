from abc import ABC, abstractmethod

from invoice_reader.domain import File


class IFileRepository(ABC):
    @abstractmethod
    def store(self, file: File) -> None:
        pass

    @abstractmethod
    def delete(self, file_path: str) -> None:
        pass

    @abstractmethod
    def get_url(self, file_path: str) -> str:
        pass

    @abstractmethod
    def create_path(self, filename: str) -> str:
        pass
