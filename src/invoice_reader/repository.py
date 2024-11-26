from abc import ABC, abstractmethod
from typing import TypeVar

import sqlmodel

from invoice_reader.models import InvoiceModel, UserModel
from invoice_reader.schemas import InvoiceSchema, UserSchema
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


class InvoiceRepository(Repository[InvoiceSchema]):
    def __init__(self, session: sqlmodel.Session):
        self.session = session

    def add(self, id_: str, user_id: str, invoice_data: InvoiceSchema, s3_path: str) -> str:
        existing_invoice = self.session.exec(
            sqlmodel.select(InvoiceModel)
            .where(InvoiceModel.invoice_number == invoice_data.invoice_number)
        ).first()
        if existing_invoice:
            raise Exception("Existing invoice in the database. Process aborted.")
        invoice_model = InvoiceModel(
            file_id=id_, user_id=user_id, s3_path=s3_path, **invoice_data.model_dump()
        )
        self.session.add(invoice_model)
        self.session.commit()
        self.session.refresh(invoice_model)
        LOGGER.info("Invoice %s added to database. Metadata: %s", id_, invoice_model)

    def update(self, id_: str, invoice_data: InvoiceSchema) -> None:
        invoice_model = self.session.exec(
            sqlmodel.select(InvoiceModel).where(InvoiceModel.file_id == id_)
        ).one()
        invoice_model.sqlmodel_update(invoice_data)
        self.session.add(invoice_model)
        self.session.commit()
        self.session.refresh(invoice_model)
        LOGGER.info("Existing invoice %s data updated with new data: %s", id_, invoice_data)

    def get(self, id_: str) -> InvoiceSchema | None:
        invoice_model = self.session.exec(
            sqlmodel.select(InvoiceModel.file_id == id_)
        ).one_or_none()
        invoice = InvoiceSchema.model_validate(invoice_model.model_dump())
        LOGGER.info("Invoice data retrieved from database: %s", invoice)
        return invoice

    def delete(self, id_: str) -> None:
        invoice_model = self.session.exec(sqlmodel.select(InvoiceModel.file_id == id_)).one()
        self.session.delete(invoice_model)
        self.session.commit()
        LOGGER.info("Invoice %s deleted from database.", id_)

    def get_all(self, limit: int = 10) -> list[InvoiceSchema]:
        invoice_models = self.session.exec(sqlmodel.select(InvoiceModel).limit(limit)).all()
        invoices = [InvoiceSchema(**invoice_model.model_dump()) for invoice_model in invoice_models]
        LOGGER("List of invoices returned from database: %s", invoices)
        return invoice_models

    def get_by_invoice_number(self, invoice_number: str) -> InvoiceModel | None:
        invoice_model = self.session.exec(
            sqlmodel.select(InvoiceModel)
            .where(InvoiceModel.invoice_number == invoice_number)
        ).one_or_none()
        if invoice_model:
            invoice = InvoiceSchema.model_validate(invoice_model.model_dump())
            LOGGER.info("Invoice data retrieved from database: %s", invoice)
            return invoice


class UserRepository(Repository):
    def __init__(self, session: sqlmodel.Session):
        self.session = session

    def add(self, user: UserSchema):
        user_model = UserModel(**user.model_dump())
        self.session.add(user_model)
        self.session.commit()
        self.session.refresh(user_model)
        LOGGER.info("New user added to database: %s", user_model)

    def update(self, id_: str, user_data: UserSchema) -> None:
        user_model = self.session.exec(
            sqlmodel.select(UserModel).where(UserModel.user_id == id_)
        ).one()
        user_model.sqlmodel_update(user_model)
        self.session.add(user_model)
        self.session.commit()
        self.session.refresh(user_model)
        LOGGER.info("Existing user %s udpated: %s", id_, user_model)

    def get(self, id_: str) -> UserSchema:
        user_model = self.session.exec(sqlmodel.select(UserModel.file_id == id_)).one()
        user_data = UserSchema.model_validate(user_model.model_dump())
        LOGGER.info("User data retrieved from database: %s", user_data)
        return user_data

    def delete(self, id_: str) -> None:
        user_model = self.session.exec(sqlmodel.select(UserModel.file_id == id_)).one()
        self.session.delete(user_model)
        self.session.commit()
        LOGGER.info("Invoice %s deleted from database.", id_)

    def get_all(self, limit: int = 10) -> list[UserSchema]:
        user_model = self.session.exec(sqlmodel.select(UserModel).limit(limit)).all()
        users = [UserSchema(**user_model.model_dump()) for user_model in user_model]
        LOGGER("List of users returned from database: %s", users)
        return users


    def get_by_username(self, username: str) -> UserSchema | None:
        user_model = self.session.exec(
            sqlmodel.select(UserModel)
            .where(UserModel.username == username)
        ).one_or_none()
        if user_model:
            user = UserSchema.model_validate(user_model.model_dump())
            LOGGER.info("User data retrieved from database: %s", user)
            return user
    

    def get_user_by_email(self, email: str) -> UserSchema | None:
        user_model = self.session.exec(
            sqlmodel.select(UserModel)
            .where(UserModel.email == email)
        ).one_or_none()
        if user_model:
            user = UserSchema.model_validate(user_model.model_dump())
            LOGGER.info("User data retrieved from database: %s", user)
            return user