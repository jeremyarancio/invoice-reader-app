import type {
    Client,
    ClientData,
    GetClient,
    UpdateClient,
} from "@/schemas/client";

export function mapGetClientToClient(getClient: GetClient): Client {
    return {
        id: getClient.client_id,
        city: getClient.data.city,
        clientName: getClient.data.client_name,
        country: getClient.data.country,
        streetAddress: getClient.data.street_address,
        streetNumber: getClient.data.street_number,
        zipcode: getClient.data.zipcode,
        totalRevenue: getClient.total_revenue,
        nInvoices: getClient.n_invoices,
    };
}

export function mapClientToUpdateClient(clientData: ClientData): UpdateClient {
    return {
        data: {
            client_name: clientData.clientName,
            street_number: clientData.streetNumber,
            street_address: clientData.streetAddress,
            zipcode: clientData.zipcode,
            city: clientData.city,
            country: clientData.country,
        },
    };
}
