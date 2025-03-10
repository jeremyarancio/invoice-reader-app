import uuid
from typing import Sequence

import sqlmodel

from invoice_reader.app.exceptions import EXISTING_INVOICE_EXCEPTION
from invoice_reader.models import ClientModel, InvoiceModel, UserModel
from invoice_reader.schemas import client_schema, invoice_schema, user_schema
from invoice_reader.utils.logger import get_logger

LOGGER = get_logger(__name__)


class InvoiceRepository:
    def __init__(self, session: sqlmodel.Session):
        self.session = session

    def add(
        self,
        id_: uuid.UUID,
        user_id: uuid.UUID,
        client_id: uuid.UUID,
        invoice_data: invoice_schema.Invoice,
        s3_path: str,
    ) -> None:
        existing_invoice = self.session.exec(
            sqlmodel.select(InvoiceModel)
            .where(InvoiceModel.invoice_number == invoice_data.invoice_number)
            .where(InvoiceModel.user_id == user_id)
        ).first()
        if existing_invoice:
            raise EXISTING_INVOICE_EXCEPTION
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

    def update(self, invoice_id: uuid.UUID, invoice: invoice_schema.Invoice) -> None:
        invoice_model = self.session.exec(
            sqlmodel.select(InvoiceModel).where(InvoiceModel.file_id == invoice_id)
        ).one()
        invoice_model.sqlmodel_update(invoice)
        self.session.add(invoice_model)
        self.session.commit()
        self.session.refresh(invoice_model)

    def get(
        self, file_id: uuid.UUID, user_id: uuid.UUID
    ) -> invoice_schema.InvoiceGetResponse:
        invoice_model = self.session.exec(
            sqlmodel.select(InvoiceModel).where(
                InvoiceModel.file_id == file_id and InvoiceModel.user_id == user_id
            )
        ).one()
        invoice_data = invoice_schema.Invoice.model_validate(invoice_model.model_dump())
        invoice_response = invoice_schema.InvoiceGetResponse(
            invoice_id=file_id,
            client_id=invoice_model.client_id,
            s3_path=invoice_model.s3_path,
            data=invoice_data,
        )
        LOGGER.info("Invoice data retrieved from database: %s", invoice_response)
        return invoice_response

    def delete(self, file_id: uuid.UUID, user_id: uuid.UUID) -> None:
        invoice_model = self.session.exec(
            sqlmodel.select(InvoiceModel).where(
                InvoiceModel.file_id == file_id and InvoiceModel.user_id == user_id
            )
        ).one()
        self.session.delete(invoice_model)
        self.session.commit()

    def get_all(self, user_id: uuid.UUID) -> list[invoice_schema.InvoiceGetResponse]:
        invoice_responses = []
        invoice_models = self.session.exec(
            sqlmodel.select(InvoiceModel).where(InvoiceModel.user_id == user_id)
        ).all()
        for invoice_model in invoice_models:
            invoice_data = invoice_schema.Invoice.model_validate(
                invoice_model.model_dump()
            )
            invoice_responses.append(
                invoice_schema.InvoiceGetResponse(
                    invoice_id=invoice_model.file_id,
                    client_id=invoice_model.client_id,
                    s3_path=invoice_model.s3_path,
                    data=invoice_data,
                )
            )
        LOGGER.info(
            "List of invoices returned from database. Number of invoices: %s",
            len(invoice_responses),
        )
        return invoice_responses

    def get_by_invoice_number(
        self, invoice_number: str
    ) -> invoice_schema.Invoice | None:
        invoice_model = self.session.exec(
            sqlmodel.select(InvoiceModel).where(
                InvoiceModel.invoice_number == invoice_number
            )
        ).one_or_none()
        if invoice_model:
            invoice = invoice_schema.Invoice.model_validate(invoice_model.model_dump())
            LOGGER.info("Invoice data retrieved from database: %s", invoice)
            return invoice

    def get_by_user_id(self, user_id: uuid.UUID) -> invoice_schema.Invoice | None:
        # DUPLICATE WITH other get_by
        invoice_model = self.session.exec(
            sqlmodel.select(InvoiceModel).where(InvoiceModel.user_id == user_id)
        ).one_or_none()
        if invoice_model:
            invoice = invoice_schema.Invoice.model_validate(invoice_model.model_dump())
            LOGGER.info("Invoice data retrieved from database: %s", invoice)
            return invoice


class UserRepository:
    def __init__(self, session: sqlmodel.Session):
        self.session = session

    def add(self, user: user_schema.User):
        user_model = UserModel(**user.model_dump())
        self.session.add(user_model)
        self.session.commit()
        self.session.refresh(user_model)
        LOGGER.info("New user added to database: %s", user_model)

    def update(self, id_: str, user_data: user_schema.User) -> None:
        user_model = self.session.exec(
            sqlmodel.select(UserModel).where(UserModel.user_id == id_)
        ).one()
        user_model.sqlmodel_update(user_model)
        self.session.add(user_model)
        self.session.commit()
        self.session.refresh(user_model)
        LOGGER.info("Existing user %s udpated: %s", id_, user_model)

    def delete(self, user_id: uuid.UUID) -> None:
        user_model = self.session.exec(
            sqlmodel.select(UserModel).where(UserModel.user_id == user_id)
        ).one()
        self.session.delete(user_model)
        self.session.commit()

    def get_all(self, limit: int = 10) -> list[user_schema.User]:
        users_model = self.session.exec(sqlmodel.select(UserModel).limit(limit)).all()
        users = [
            user_schema.User(**user_model.model_dump()) for user_model in users_model
        ]
        LOGGER.info("List of users returned from database: %s", users)
        return users

    def get_user_by_email(self, email: str) -> user_schema.User | None:
        user_model = self.session.exec(
            sqlmodel.select(UserModel).where(UserModel.email == email)
        ).one_or_none()
        if user_model:
            user = user_schema.User.model_validate(user_model.model_dump())
            LOGGER.info("User data retrieved from database: %s", user)
            return user
        else:
            return None


class ClientRepository:
    def __init__(self, session: sqlmodel.Session):
        self.session = session

    def get(self, user_id: uuid.UUID, client_id: uuid.UUID) -> ClientModel | None:
        client_model = self.session.exec(
            sqlmodel.select(ClientModel).where(
                ClientModel.client_id == client_id and ClientModel.user_id == user_id
            )
        ).one_or_none()
        return client_model

    def add(self, user_id: uuid.UUID, client: client_schema.Client) -> None:
        client_model = ClientModel(user_id=user_id, **client.model_dump())
        self.session.add(client_model)
        self.session.commit()

    def get_all(self, user_id: uuid.UUID, limit: int) -> Sequence[ClientModel]:
        client_models = self.session.exec(
            sqlmodel.select(ClientModel)
            .where(ClientModel.user_id == user_id)
            .limit(limit)
        ).all()

        return client_models

    def delete(self, client_id: uuid.UUID, user_id: uuid.UUID):
        client_model = self.session.exec(
            sqlmodel.select(ClientModel).where(
                ClientModel.client_id == client_id and ClientModel.user_id == user_id
            )
        ).one()
        self.session.delete(client_model)
        self.session.commit()

    def get_by_name(
        self, user_id: uuid.UUID, client_name: str
    ) -> client_schema.Client | None:
        client_model = self.session.exec(
            sqlmodel.select(ClientModel).where(
                ClientModel.client_name == client_name
                and ClientModel.user_id == user_id
            )
        ).one_or_none()
        if client_model:
            client = client_schema.Client.model_validate(client_model.model_dump())
            return client
