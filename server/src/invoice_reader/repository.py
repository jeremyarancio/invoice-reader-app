import uuid
from typing import Sequence

import sqlmodel

from invoice_reader.app.exceptions import (
    CLIENT_NOT_FOUND,
    EXISTING_INVOICE_EXCEPTION,
    INVOICE_NOT_FOUND,
    USER_NOT_FOUND_EXCEPTION,
)
from invoice_reader.models import (
    ClientModel,
    CurrencyModel,
    InvoiceModel,
    UserModel,
)
from invoice_reader.schemas.clients import ClientUpdate
from invoice_reader.utils.logger import get_logger

LOGGER = get_logger()


class InvoiceRepository:
    def __init__(self, session: sqlmodel.Session):
        self.session = session

    def add(
        self,
        user_id: uuid.UUID,
        invoice_model: InvoiceModel,
    ) -> None:
        existing_invoice = self.session.exec(
            sqlmodel.select(InvoiceModel).where(
                InvoiceModel.invoice_number == invoice_model.invoice_number,
                InvoiceModel.user_id == user_id,
            )
        ).first()
        if existing_invoice:
            raise EXISTING_INVOICE_EXCEPTION
        self.session.add(invoice_model)
        self.session.commit()
        self.session.refresh(invoice_model)

    def update(self, invoice_id: uuid.UUID, values_to_update: dict) -> None:
        invoice_model = self.session.exec(
            sqlmodel.select(InvoiceModel).where(InvoiceModel.file_id == invoice_id)
        ).one_or_none()
        if not invoice_model:
            raise INVOICE_NOT_FOUND
        invoice_model.sqlmodel_update(values_to_update)
        self.session.add(invoice_model)
        self.session.commit()
        self.session.refresh(invoice_model)

    def get(self, file_id: uuid.UUID, user_id: uuid.UUID) -> InvoiceModel | None:
        invoice_model = self.session.exec(
            sqlmodel.select(InvoiceModel).where(
                InvoiceModel.file_id == file_id, InvoiceModel.user_id == user_id
            )
        ).one_or_none()
        return invoice_model

    def delete(self, file_id: uuid.UUID, user_id: uuid.UUID) -> None:
        invoice_model = self.session.exec(
            sqlmodel.select(InvoiceModel).where(
                InvoiceModel.file_id == file_id, InvoiceModel.user_id == user_id
            )
        ).one_or_none()
        if not invoice_model:
            raise INVOICE_NOT_FOUND
        self.session.delete(invoice_model)
        self.session.commit()

    def get_all(self, user_id: uuid.UUID) -> Sequence[InvoiceModel]:
        invoice_models = self.session.exec(
            sqlmodel.select(InvoiceModel).where(InvoiceModel.user_id == user_id)
        ).all()
        return invoice_models

    def get_by_invoice_number(
        self,
        invoice_number: str,
        user_id: uuid.UUID,
    ) -> InvoiceModel | None:
        invoice_model = self.session.exec(
            sqlmodel.select(InvoiceModel).where(
                InvoiceModel.invoice_number == invoice_number,
                InvoiceModel.user_id == user_id,
            )
        ).one_or_none()
        return invoice_model


class UserRepository:
    def __init__(self, session: sqlmodel.Session):
        self.session = session

    def get(self, user_id: uuid.UUID) -> UserModel | None:
        user_model = self.session.exec(
            sqlmodel.select(UserModel).where(UserModel.user_id == user_id)
        ).one_or_none()
        return user_model

    def add(self, user_model: UserModel) -> None:
        self.session.add(user_model)
        self.session.commit()
        self.session.refresh(user_model)

    def update(self, id_: str) -> None:
        user_model = self.session.exec(
            sqlmodel.select(UserModel).where(UserModel.user_id == id_)
        ).one()
        user_model.sqlmodel_update(user_model)
        self.session.add(user_model)
        self.session.commit()
        self.session.refresh(user_model)

    def delete(self, user_id: uuid.UUID) -> None:
        user_model = self.session.exec(
            sqlmodel.select(UserModel).where(UserModel.user_id == user_id)
        ).one_or_none()
        if not user_model:
            raise USER_NOT_FOUND_EXCEPTION
        self.session.delete(user_model)
        self.session.commit()

    def get_all(self, limit: int = 10) -> Sequence[UserModel]:
        user_models = self.session.exec(sqlmodel.select(UserModel).limit(limit)).all()
        return user_models

    def get_user_by_email(self, email: str) -> UserModel | None:
        user_model = self.session.exec(
            sqlmodel.select(UserModel).where(UserModel.email == email)
        ).one_or_none()
        return user_model


class ClientRepository:
    def __init__(self, session: sqlmodel.Session):
        self.session = session

    def get(self, user_id: uuid.UUID, client_id: uuid.UUID) -> ClientModel | None:
        client_model = self.session.exec(
            sqlmodel.select(ClientModel).where(
                ClientModel.client_id == client_id, ClientModel.user_id == user_id
            )
        ).one_or_none()
        return client_model

    def add(self, client_model: ClientModel) -> None:
        self.session.add(client_model)
        self.session.commit()

    def get_all(
        self, user_id: uuid.UUID, limit: int | None = None
    ) -> Sequence[ClientModel]:
        client_models = self.session.exec(
            sqlmodel.select(ClientModel)
            .where(ClientModel.user_id == user_id)
            .limit(limit)
            if limit
            else sqlmodel.select(ClientModel).where(ClientModel.user_id == user_id)
        ).all()
        return client_models

    def delete(self, client_id: uuid.UUID, user_id: uuid.UUID):
        client_model = self.session.exec(
            sqlmodel.select(ClientModel).where(
                ClientModel.client_id == client_id, ClientModel.user_id == user_id
            )
        ).one_or_none()
        if not client_model:
            raise CLIENT_NOT_FOUND
        self.session.delete(client_model)
        self.session.commit()

    def get_by_name(self, user_id: uuid.UUID, client_name: str) -> ClientModel | None:
        client_model = self.session.exec(
            sqlmodel.select(ClientModel).where(
                ClientModel.client_name == client_name, ClientModel.user_id == user_id
            )
        ).one_or_none()
        return client_model

    def update(self, client_id: uuid.UUID, values_to_update: dict) -> None:
        existing_client = self.session.exec(
            sqlmodel.select(ClientModel).where(ClientModel.client_id == client_id)
        ).one_or_none()
        if not existing_client:
            raise CLIENT_NOT_FOUND
        existing_client.sqlmodel_update(values_to_update)
        self.session.add(existing_client)
        self.session.commit()


class CurrencyRepository:
    def __init__(self, session: sqlmodel.Session) -> None:
        self.session = session

    def get_all(self) -> Sequence[CurrencyModel]:
        return self.session.exec(sqlmodel.select(CurrencyModel)).all()
