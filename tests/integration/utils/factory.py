"""Function to fill the test database with elements.
Useful for GET and POST requests.
"""

from sqlmodel import Session

from .fixtures import user

from invoice_reader.schemas import (
    User,
)
from invoice_reader.models import UserModel, InvoiceModel, ClientModel


def add_to_db() -> None:
    pass


def add_user_to_db(user: User, session: Session) -> None:
    """
    Args:
        user_id (uuid.UUID | None): Some tests require a specific user_id. Deprecated.
    """
    user_model = UserModel(**user.model_dump())
    session.add(user_model)
    session.commit()


def add_invoices_to_db(invoice_models: list[InvoiceModel], session: Session) -> None:
    session.add_all(invoice_models)
    session.commit()


def add_clients(
    client_models: list[ClientModel],
    session: Session,
) -> None:
    session.add_all(client_models)
    session.commit()

