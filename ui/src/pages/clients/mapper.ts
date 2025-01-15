import { Client, CreateClient, GetClient } from "./types";

export function mapGetClientToClient(getClient: GetClient): Client {
    return {
        id: getClient.client_id,
        city: getClient.city,
        name: getClient.client_name,
        country: getClient.country,
        streetAddress: getClient.street_address,
        streetNumber: getClient.street_number,
        zipcode: getClient.zipcode,
    };
}

export function mapClientToCreateClient(
    client: Omit<Client, "id">
): CreateClient {
    return {
        client_name: client.name,
        city: client.city,
        country: client.country,
        street_address: client.streetAddress,
        street_number: client.streetNumber,
        zipcode: client.zipcode,
    };
}
