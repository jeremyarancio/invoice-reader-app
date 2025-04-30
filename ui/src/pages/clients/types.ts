export interface Client {
    id: string;
    name: string;
    streetNumber: number;
    streetAddress: string;
    zipcode: number;
    city: string;
    country: string;
    totalRevenu: number;
}

export interface CreateClient {
    client_name: string;
    street_number: number;
    street_address: string;
    zipcode: number;
    city: string;
    country: string;
}

export interface GetPagedClients {
    per_page: number;
    total: number;
    data: GetClient[];
}

export interface GetClient {
    client_id: string;
    client_name: string;
    street_number: number;
    street_address: string;
    zipcode: number;
    city: string;
    country: string;
    total_revenu: number;
}

export interface UpdateClient {
    id: string;
    client: {
        client_name: string;
        street_number: number;
        street_address: string;
        zipcode: number;
        city: string;
        country: string;
    };
}
