from abc import ABC, abstractmethod

from invoice_reader.domain.user import UUID, User


class IUserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> None:
        pass

    @abstractmethod
    def update(self, user: User) -> None:
        pass

    @abstractmethod
    def get(self, user_id: UUID) -> User | None:
        pass

    @abstractmethod
    def delete(self, user_id: UUID) -> None:
        pass

    @abstractmethod
    def get_all(self) -> list[User]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        pass
