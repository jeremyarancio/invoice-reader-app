from uuid import UUID

from sqlmodel import Session, select

from invoice_reader.domain.client import Client
from invoice_reader.infrastructure.models.client import ClientModel
from invoice_reader.services.interfaces.repositories import IClientRepository


class InMemoryClientRepository(IClientRepository):
    def __init__(self):
        self.clients: dict[UUID, Client] = {}

    def add(self, client: Client) -> None:
        self.clients[client.id_] = client

    def get(self, client_id: UUID) -> Client | None:
        return self.clients.get(client_id)

    def update(self, client: Client) -> None:
        if client.id_ in self.clients:
            self.clients[client.id_] = client

    def delete(self, client_id: UUID) -> None:
        if client_id in self.clients:
            self.clients.pop(client_id)

    def get_all(self, user_id: UUID) -> list[Client]:
        return [client for client in self.clients.values() if client.user_id == user_id]

    def get_by_name(self, user_id: UUID, client_name: str) -> Client | None:
        for client in self.clients.values():
            if client.user_id == user_id and client.client_name == client_name:
                return client


class SQLModelClientRepository(IClientRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_model(self, client: Client) -> ClientModel:
        """Convert domain entity to infrastructure model."""
        return ClientModel(
            client_id=client.id_,
            user_id=client.user_id,
            client_name=client.client_name,
            street_number=client.street_number,
            street_address=client.street_address,
            zipcode=client.zipcode,
            city=client.city,
            country=client.country,
        )

    def _to_entity(self, model: ClientModel) -> Client:
        """Convert infrastructure model to domain entity."""
        return Client(
            id_=model.client_id,
            user_id=model.user_id,
            client_name=model.client_name,
            street_number=model.street_number,
            street_address=model.street_address,
            zipcode=model.zipcode,
            city=model.city,
            country=model.country,
        )

    def add(self, client: Client) -> None:
        client_model = self._to_model(client)
        self.session.add(client_model)
        self.session.commit()

    def get(self, client_id: UUID) -> Client | None:
        client_model = self.session.exec(
            select(ClientModel).where(ClientModel.client_id == client_id)
        ).one_or_none()
        return self._to_entity(client_model) if client_model else None

    def update(self, client: Client) -> None:
        existing_client_model = self.session.exec(
            select(ClientModel).where(ClientModel.client_id == client.id_)
        ).one()

        # Update existing model with new values
        updated_data = self._to_model(client).model_dump(exclude={"id"})  # Assuming SQLModel
        for key, value in updated_data.items():
            setattr(existing_client_model, key, value)

        self.session.add(existing_client_model)
        self.session.commit()

    def delete(self, client_id: UUID) -> None:
        client_model = self.session.exec(
            select(ClientModel).where(ClientModel.client_id == client_id)
        ).one()
        if client_model:
            self.session.delete(client_model)
            self.session.commit()

    def get_all(self, user_id: UUID) -> list[Client]:
        client_models = self.session.exec(
            select(ClientModel).where(ClientModel.user_id == user_id)
        ).all()
        return [self._to_entity(model) for model in client_models]

    def get_by_name(self, user_id: UUID, client_name: str) -> Client | None:
        client_model = self.session.exec(
            select(ClientModel).where(
                ClientModel.user_id == user_id, ClientModel.client_name == client_name
            )
        ).one_or_none()
        return self._to_entity(client_model) if client_model else None
