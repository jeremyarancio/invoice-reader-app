export interface Client {
    id: string;
    clientName: string;
    streetNumber: string;
    streetAddress: string;
    zipcode: string;
    city: string;
    country: string;
    totalRevenue: number;
    nInvoices: number;
}

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
    total_revenue: number;
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
    client_name: string;
    street_number: string;
    street_address: string;
    zipcode: string;
    city: string;
    country: string;
}
