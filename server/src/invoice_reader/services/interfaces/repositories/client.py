from abc import ABC, abstractmethod
from uuid import UUID

from invoice_reader.domain.clients import Client, ClientID


class IClientRepository(ABC):
    @abstractmethod
    def add(self, client: Client) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, client: Client) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, client_id: ClientID) -> Client | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, client_id: ClientID) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, user_id: UUID) -> list[Client]:
        raise NotImplementedError

    @abstractmethod
    def get_by_name(self, user_id: UUID, client_name: str) -> Client | None:
        raise NotImplementedError
