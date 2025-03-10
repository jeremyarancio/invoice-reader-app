from invoice_reader.core.stats import compute_total_revenu_per_client
from invoice_reader.models import ClientModel
from invoice_reader.schemas import client_schema


def map_client_model_to_client(
    client_model: ClientModel,
) -> client_schema.ClientPresenter:
    return client_schema.ClientPresenter(
        client_id=client_model.client_id,
        country=client_model.country,
        city=client_model.city,
        client_name=client_model.client_name,
        street_address=client_model.street_address,
        street_number=client_model.street_number,
        zipcode=client_model.zipcode,
        total_revenu=compute_total_revenu_per_client(client_model),
    )


def map_client_models_to_clients(
    client_models: list[ClientModel],
) -> list[client_schema.Client]:
    return [
        map_client_model_to_client(client_model=client_model)
        for client_model in client_models
    ]
