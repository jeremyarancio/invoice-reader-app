import type { Client, GetClient, UpdateClient } from "@/schemas/client";

export function mapGetClientToClient(getClient: GetClient): Client {
    return {
        id: getClient.client_id,
        city: getClient.data.city,
        clientName: getClient.data.client_name,
        country: getClient.data.country,
        streetAddress: getClient.data.street_address,
        streetNumber: getClient.data.street_number,
        zipcode: getClient.data.zipcode,
        totalRevenu: getClient.total_revenu,
    };
}

export function mapClientToUpdateClient(client: Client): UpdateClient {
    return {
        client_name: client.clientName,
        street_number: client.streetNumber,
        street_address: client.streetAddress,
        zipcode: client.zipcode,
        city: client.city,
        country: client.country,
        };
    };