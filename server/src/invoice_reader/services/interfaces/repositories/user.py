from abc import ABC, abstractmethod
from uuid import UUID
from typing import Sequence

from invoice_reader.domain import User


class IUserRepository(ABC):
    @abstractmethod
    def add(
        self,
        user_id: UUID,
    ) -> None:
        pass

    @abstractmethod
    def update(self, user_id: UUID, user: User) -> None:
        pass

    @abstractmethod
    def get(self, user_id: UUID) -> User | None:
        pass

    @abstractmethod
    def delete(self, user_id: UUID) -> None:
        pass

    @abstractmethod
    def get_all(self) -> Sequence[User]:
        pass

    @abstractmethod
    def get_by_username(
        self,
        username: str,
    ) -> User | None:
        pass
