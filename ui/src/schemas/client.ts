export type ClientData = {
    clientName: string;
    streetNumber: string;
    streetAddress: string;
    zipcode: string;
    city: string;
    country: string;
};

export type Client = {
    id: string;
    totalRevenue: Record<string, number>;
    nInvoices: number;
} & ClientData;

export interface CreateClient {
    client_name: string;
    street_number: number;
    street_address: string;
    zipcode: string;
    city: string;
    country: string;
}

export interface GetPagedClients {
    page: number;
    per_page: number;
    total: number;
    clients: GetClient[];
}

export interface GetClient {
    client_id: string;
    total_revenue: Record<string, number>;
    n_invoices: number;
    data: {
        client_name: string;
        street_number: string;
        street_address: string;
        zipcode: string;
        city: string;
        country: string;
    };
}

export interface UpdateClient {
    data: {
        client_name: string;
        street_number: string;
        street_address: string;
        zipcode: string;
        city: string;
        country: string;
    };
}
