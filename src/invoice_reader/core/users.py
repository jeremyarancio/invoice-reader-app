from invoice_reader.schemas import UserSchema
from invoice_reader.repository import UserRepository


def register(user: UserSchema, repository: UserRepository) -> None:
    """Pretty simple, I know."""
    repository.add(user)