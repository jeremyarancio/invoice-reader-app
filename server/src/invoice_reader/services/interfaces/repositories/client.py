from abc import ABC, abstractmethod

from invoice_reader.domain.client import Client, ClientID
from invoice_reader.domain.user import UserID


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
    def get_all(self, user_id: UserID) -> list[Client]:
        raise NotImplementedError

    @abstractmethod
    def get_by_name(self, user_id: UserID, client_name: str) -> Client | None:
        raise NotImplementedError
