from abc import ABC, abstractmethod

from invoice_reader.domain.invoice import File


class IFileRepository(ABC):
    @abstractmethod
    def store(self, file: File) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, storage_path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_url(self, storage_path: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def create_storage_path(self, initial_path: str) -> str:
        raise NotImplementedError
