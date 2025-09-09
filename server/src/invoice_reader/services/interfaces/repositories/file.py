from abc import ABC, abstractmethod

from invoice_reader.domain import File


class IFileRepository(ABC):
    @abstractmethod
    def store(self, file: File) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, file: File) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_url(self, file: File) -> str:
        raise NotImplementedError

    @abstractmethod
    def create_storage_path(self, filename: str) -> str:
        raise NotImplementedError
