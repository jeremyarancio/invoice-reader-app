from abc import ABC, abstractmethod
from uuid import UUID
from typing import Sequence

from invoice_reader.domain import Client


class ClientRepositoryPort(ABC):
    @abstractmethod
    def add(
        self,
        user_id: UUID,
    ) -> None:
        pass

    @abstractmethod
    def update(self, client_id: UUID, client: Client) -> None:
        pass

    @abstractmethod
    def get(self, client_id: UUID, user_id: UUID) -> Client | None:
        pass

    @abstractmethod
    def delete(self, client_id: UUID, user_id: UUID) -> None:
        pass

    @abstractmethod
    def get_all(self, user_id: UUID) -> Sequence[Client]:
        pass

    @abstractmethod
    def get_by_client_number(
        self,
        client_number: str,
        user_id: UUID,
    ) -> Client | None:
        pass
