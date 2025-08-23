from abc import ABC, abstractmethod
from uuid import UUID
from typing import BinaryIO, Sequence

from invoice_reader import settings
from invoice_reader.domain import Invoice
from invoice_reader.interfaces.schemas.invoice import InvoiceCreate
from invoice_reader.repository import InvoiceRepository
from invoice_reader.services.exceptions import (
    UNPROCESSABLE_FILE,
)


class FileStoragePort(ABC):
    @abstractmethod
    def store(self, file: BinaryIO) -> None:
        pass

    @abstractmethod
    def delete(self, file_path: str) -> None:
        pass

    @abstractmethod
    def get_url(self, file_path: str) -> str:
        pass


class InvoiceRepositoryPort(ABC):
    @abstractmethod
    def add(
        self,
        user_id: UUID,
    ) -> None:
        pass

    @abstractmethod
    def update(self, invoice_id: UUID, invoice: Invoice) -> None:
        pass

    @abstractmethod
    def get(self, invoice_id: UUID, user_id: UUID) -> Invoice | None:
        pass

    @abstractmethod
    def delete(self, invoice_id: UUID, user_id: UUID) -> None:
        pass

    @abstractmethod
    def get_all(self, user_id: UUID) -> Sequence[Invoice]:
        pass

    @abstractmethod
    def get_by_invoice_number(
        self,
        invoice_number: str,
        user_id: UUID,
    ) -> Invoice | None:
        pass


class InvoiceService:
    @classmethod
    def add_invoice(
        user_id: UUID,
        file: BinaryIO,
        filename: str | None,
        invoice_create: InvoiceCreate,
        file_storage: FileStoragePort,
        invoice_repository: InvoiceRepositoryPort,
    ) -> None:
        if not filename:
            raise UNPROCESSABLE_FILE

        invoice = InvoiceMapper.map_invoice_create_to_invoice(invoice_create)
        storage.store(
            file=file,
            file_data=file_data,
            invoice=invoice,
            invoice_repository=invoice_repository,
            s3_model=s3_model,
        )
