import type { Client, GetClient, UpdateClient } from "@/schemas/client";

export function mapGetClientToClient(getClient: GetClient): Client {
    return {
        id: getClient.client_id,
        city: getClient.city,
        clientName: getClient.client_name,
        country: getClient.country,
        streetAddress: getClient.street_address,
        streetNumber: getClient.street_number,
        zipcode: getClient.zipcode,
        totalRevenu: getClient.total_revenu,
    };
}

export function mapClientToUpdateClient(client: Client): UpdateClient {
    return {
        id: client.id,
        client: {
            client_name: client.clientName,
            street_number: client.streetNumber,
            street_address: client.streetAddress,
            zipcode: client.zipcode,
            city: client.city,
            country: client.country,
        },
    };
}
