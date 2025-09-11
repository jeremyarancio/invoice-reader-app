from sqlmodel import Session, select

from invoice_reader.domain.client import Client, ClientID
from invoice_reader.domain.user import UserID
from invoice_reader.infrastructure.models.client import ClientModel
from invoice_reader.services.interfaces.repositories import IClientRepository


class SQLModelClientRepository(IClientRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, client: Client) -> None:
        client_model = ClientModel(
            client_id=client.id_,
            user_id=client.user_id,
            client_name=client.client_name,
            street_number=client.street_number,
            street_address=client.street_address,
            zipcode=client.zipcode,
            city=client.city,
            country=client.country,
        )
        self.session.add(client_model)
        self.session.commit()

    def get(self, client_id: ClientID) -> Client | None:
        client_model = self.session.exec(
            select(ClientModel).where(ClientModel.client_id == client_id)
        ).one_or_none()
        if client_model:
            return Client(
                id_=client_model.client_id,
                user_id=client_model.user_id,
                client_name=client_model.client_name,
                street_number=client_model.street_number,
                street_address=client_model.street_address,
                zipcode=client_model.zipcode,
                city=client_model.city,
                country=client_model.country,
            )

    def update(self, client: Client) -> None:
        pass

    def delete(self, client_id: ClientID) -> None:
        client_model = self.session.exec(
            select(ClientModel).where(ClientModel.client_id == client_id)
        ).one()
        if client_model:
            self.session.delete(client_model)
            self.session.commit()

    def get_all(self, user_id: UserID) -> list[Client]:
        client_models = self.session.exec(
            select(ClientModel).where(ClientModel.user_id == user_id)
        ).all()
        return [
            Client(
                id_=client_model.client_id,
                user_id=client_model.user_id,
                client_name=client_model.client_name,
                street_number=client_model.street_number,
                street_address=client_model.street_address,
                zipcode=client_model.zipcode,
                city=client_model.city,
                country=client_model.country,
            )
            for client_model in client_models
        ]

    def get_by_name(self, user_id: UserID, client_name: str) -> Client | None:
        client_model = self.session.exec(
            select(ClientModel).where(
                ClientModel.user_id == user_id, ClientModel.client_name == client_name
            )
        ).one_or_none()
        if client_model:
            return Client(
                id_=client_model.client_id,
                user_id=client_model.user_id,
                client_name=client_model.client_name,
                street_number=client_model.street_number,
                street_address=client_model.street_address,
                zipcode=client_model.zipcode,
                city=client_model.city,
                country=client_model.country,
            )
