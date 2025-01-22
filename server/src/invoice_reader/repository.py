import uuid

import sqlmodel

from invoice_reader.app.exceptions import EXISTING_INVOICE_EXCEPTION
from invoice_reader.models import ClientModel, InvoiceModel, UserModel
from invoice_reader.schemas import Client, Invoice, InvoiceGetResponse, User
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
        invoice_data: Invoice,
        s3_path: str,
    ) -> str:
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
        LOGGER.info("Invoice %s added to database. Metadata: %s", id_, invoice_model)

    def update(self, invoice_id: uuid.UUID, invoice: Invoice) -> None:
        invoice_model = self.session.exec(
            sqlmodel.select(InvoiceModel).where(InvoiceModel.file_id == invoice_id)
        ).one()
        invoice_model.sqlmodel_update(invoice)
        self.session.add(invoice_model)
        self.session.commit()
        self.session.refresh(invoice_model)

    def get(self, file_id: uuid.UUID, user_id: uuid.UUID) -> InvoiceGetResponse:
        invoice_model = self.session.exec(
            sqlmodel.select(InvoiceModel).where(
                InvoiceModel.file_id == file_id and InvoiceModel.user_id == user_id
            )
        ).one()
        invoice_data = Invoice.model_validate(invoice_model.model_dump())
        invoice_response = InvoiceGetResponse(
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

    def get_all(self, user_id: uuid.UUID) -> list[InvoiceGetResponse]:
        invoice_responses = []
        invoice_models = self.session.exec(
            sqlmodel.select(InvoiceModel).where(InvoiceModel.user_id == user_id)
        ).all()
        for invoice_model in invoice_models:
            invoice_data = Invoice.model_validate(invoice_model.model_dump())
            invoice_responses.append(
                InvoiceGetResponse(
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

    def get_by_invoice_number(self, invoice_number: str) -> Invoice | None:
        invoice_model = self.session.exec(
            sqlmodel.select(InvoiceModel).where(
                InvoiceModel.invoice_number == invoice_number
            )
        ).one_or_none()
        if invoice_model:
            invoice = Invoice.model_validate(invoice_model.model_dump())
            LOGGER.info("Invoice data retrieved from database: %s", invoice)
            return invoice

    def get_by_user_id(self, user_id: uuid.UUID) -> Invoice | None:
        # DUPLICATE WITH other get_by
        invoice_model = self.session.exec(
            sqlmodel.select(InvoiceModel).where(InvoiceModel.user_id == user_id)
        ).one_or_none()
        if invoice_model:
            invoice = Invoice.model_validate(invoice_model.model_dump())
            LOGGER.info("Invoice data retrieved from database: %s", invoice)
            return invoice


class UserRepository:
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

    def delete(self, user_id: uuid.UUID) -> None:
        user_model = self.session.exec(
            sqlmodel.select(UserModel).where(UserModel.user_id == user_id)
        ).one()
        self.session.delete(user_model)
        self.session.commit()

    def get_all(self, limit: int = 10) -> list[User]:
        users_model = self.session.exec(sqlmodel.select(UserModel).limit(limit)).all()
        users = [User(**user_model.model_dump()) for user_model in users_model]
        LOGGER("List of users returned from database: %s", users)
        return users

    def get_user_by_email(self, email: str) -> User | None:
        user_model = self.session.exec(
            sqlmodel.select(UserModel).where(UserModel.email == email)
        ).one_or_none()
        if user_model:
            user = User.model_validate(user_model.model_dump())
            LOGGER.info("User data retrieved from database: %s", user)
            return user
        else:
            return None


class ClientRepository:
    def __init__(self, session: sqlmodel.Session):
        self.session = session

    def add(self, user_id: uuid.UUID, client: Client) -> None:
        client_model = ClientModel(user_id=user_id, **client.model_dump())
        self.session.add(client_model)
        self.session.commit()

    def get(self, user_id: uuid.UUID, client_id: uuid.UUID) -> Client:
        pass

    def get_all(self, user_id: uuid.UUID, limit: int) -> list[Client]:
        clients_model = self.session.exec(
            sqlmodel.select(ClientModel).where(ClientModel.user_id == user_id)
        ).all()
        clients = [
            Client.model_validate(client_model.model_dump())
            for client_model in clients_model
        ]
        return clients

    def update():
        pass

    def delete(self, client_id: uuid.UUID, user_id: uuid.UUID):
        client_model = self.session.exec(
            sqlmodel.select(ClientModel).where(
                ClientModel.client_id == client_id and ClientModel.user_id == user_id
            )
        ).one()
        self.session.delete(client_model)
        self.session.commit()

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
