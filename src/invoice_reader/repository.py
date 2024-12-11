import uuid
from abc import ABC, abstractmethod
from typing import TypeVar

import sqlmodel

from invoice_reader.models import ClientModel, InvoiceModel, UserModel
from invoice_reader.schemas import Client, Invoice, InvoiceResponse, User
from invoice_reader.utils.logger import get_logger

LOGGER = get_logger(__name__)

T = TypeVar("T")


class Repository[T](ABC):
    @abstractmethod
    def get(self, id_: str) -> T:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id_: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, **kwargs: object) -> None:
        raise NotImplementedError

    @abstractmethod
    def add(self, id_: str, **kwargs: object) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, limit: int) -> list[T]:
        raise NotImplementedError


class InvoiceRepository(Repository[Invoice]):
    def __init__(self, session: sqlmodel.Session):
        self.session = session

    def add(
        self,
        id_: uuid.UUID,
        user_id: uuid.UUID,
        client_id: uuid.UUID,
        invoice_data: Invoice,
        s3_path: str,
    ) -> str:
        existing_invoice = self.session.exec(
            sqlmodel.select(InvoiceModel).where(
                InvoiceModel.invoice_number == invoice_data.invoice_number
            )
        ).first()
        if existing_invoice:
            raise Exception("Existing invoice in the database. Process aborted.")
        invoice_model = InvoiceModel(
            file_id=id_,
            user_id=user_id,
            client_id=client_id,
            s3_path=s3_path,
            **invoice_data.model_dump(),
        )
        self.session.add(invoice_model)
        self.session.commit()
        self.session.refresh(invoice_model)
        LOGGER.info("Invoice %s added to database. Metadata: %s", id_, invoice_model)

    def update(self, id_: str, invoice_data: Invoice) -> None:
        invoice_model = self.session.exec(
            sqlmodel.select(InvoiceModel).where(InvoiceModel.file_id == id_)
        ).one()
        invoice_model.sqlmodel_update(invoice_data)
        self.session.add(invoice_model)
        self.session.commit()
        self.session.refresh(invoice_model)
        LOGGER.info(
            "Existing invoice %s data updated with new data: %s", id_, invoice_data
        )

    def get(self, file_id: uuid.UUID, user_id: uuid.UUID) -> InvoiceResponse:
        invoice_model = self.session.exec(
            sqlmodel.select(InvoiceModel).where(
                InvoiceModel.file_id == file_id and InvoiceModel.user_id == user_id
            )
        ).one()
        invoice_data = Invoice.model_validate(invoice_model.model_dump())
        invoice_response = InvoiceResponse(
            file_id=file_id, s3_path=invoice_model.s3_path, data=invoice_data
        )
        LOGGER.info("Invoice data retrieved from database: %s", invoice_response)
        return invoice_response

    def delete(self, id_: str) -> None:
        invoice_model = self.session.exec(
            sqlmodel.select(InvoiceModel.file_id == id_)
        ).one()
        self.session.delete(invoice_model)
        self.session.commit()
        LOGGER.info("Invoice %s deleted from database.", id_)

    def get_all(self, user_id: uuid.UUID) -> list[InvoiceResponse]:
        invoice_responses = []
        invoice_models = self.session.exec(
            sqlmodel.select(InvoiceModel).where(InvoiceModel.user_id == user_id)
        ).all()
        for invoice_model in invoice_models:
            invoice_data = Invoice.model_validate(invoice_model.model_dump())
            invoice_responses.append(
                InvoiceResponse(
                    file_id=invoice_model.file_id,
                    s3_path=invoice_model.s3_path,
                    data=invoice_data,
                )
            )
        LOGGER.info(
            "List of invoices returned from database. Number of invoices: %s",
            len(invoice_responses),
        )
        return invoice_responses

    def get_by_invoice_number(self, invoice_number: str) -> InvoiceModel | None:
        invoice_model = self.session.exec(
            sqlmodel.select(InvoiceModel).where(
                InvoiceModel.invoice_number == invoice_number
            )
        ).one_or_none()
        if invoice_model:
            invoice = Invoice.model_validate(invoice_model.model_dump())
            LOGGER.info("Invoice data retrieved from database: %s", invoice)
            return invoice


class UserRepository(Repository):
    def __init__(self, session: sqlmodel.Session):
        self.session = session

    def add(self, user: User):
        user_model = UserModel(**user.model_dump())
        self.session.add(user_model)
        self.session.commit()
        self.session.refresh(user_model)
        LOGGER.info("New user added to database: %s", user_model)

    def update(self, id_: str, user_data: User) -> None:
        user_model = self.session.exec(
            sqlmodel.select(UserModel).where(UserModel.user_id == id_)
        ).one()
        user_model.sqlmodel_update(user_model)
        self.session.add(user_model)
        self.session.commit()
        self.session.refresh(user_model)
        LOGGER.info("Existing user %s udpated: %s", id_, user_model)

    def get(self, id_: str) -> User:
        pass

    def delete(self, id_: str) -> None:
        pass

    def get_all(self, limit: int = 10) -> list[User]:
        user_model = self.session.exec(sqlmodel.select(UserModel).limit(limit)).all()
        users = [User(**user_model.model_dump()) for user_model in user_model]
        LOGGER("List of users returned from database: %s", users)
        return users

    def get_by_username(self, username: str) -> User | None:
        user_model = self.session.exec(
            sqlmodel.select(UserModel).where(UserModel.username == username)
        ).one_or_none()
        if user_model:
            user = User.model_validate(user_model.model_dump())
            LOGGER.info("User data retrieved from database: %s", user)
            return user

    def get_user_by_email(self, email: str) -> User | None:
        user_model = self.session.exec(
            sqlmodel.select(UserModel).where(UserModel.email == email)
        ).one_or_none()
        if user_model:
            user = User.model_validate(user_model.model_dump())
            LOGGER.info("User data retrieved from database: %s", user)
            return user


class ClientRepository(Repository):
    def __init__(self, session: sqlmodel.Session):
        self.session = session

    def add(self, user_id: uuid.UUID, client: Client) -> None:
        client_model = ClientModel(user_id=user_id, **client.model_dump())
        self.session.add(client_model)
        self.session.commit()

    def get(self, user_id: uuid.UUID, client_id: uuid.UUID) -> Client:
        pass

    def get_all(self, limit: int) -> list[Client]:
        pass

    def update():
        pass

    def delete():
        pass

    def get_by_name(self, user_id: uuid.UUID, client_name: str) -> Client | None:
        client_model = self.session.exec(
            sqlmodel.select(ClientModel).where(
                ClientModel.client_name == client_name
                and ClientModel.user_id == user_id
            )
        ).one_or_none()
        if client_model:
            client = Client.model_validate(client_model.model_dump())
            return client
