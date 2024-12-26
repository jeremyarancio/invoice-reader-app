export interface InvoiceRender {
    data: Invoice;
    clientName: string;
    paid?: boolean;
}

export interface Invoice {
    invoice_id: string;
    client_id: string;
    amount_excluding_tax: number;
    vat: number;
    currency: string;
    invoiced_date: Date;
    invoice_number: string;
}

export interface AddInvoicePayload {
    invoice: Invoice;
    client_id: string;
}

export interface UserRegistrationData {
    email: string;
    password: string;
}

export interface UserLoginData {
    email: string;
    password: string;
}

export interface InvoiceListGetProps {
    pageNumber: number;
    perPage: number;
}

export interface GetInvoicesResponse {
    page: number;
    per_page: number;
    total: number;
    data: {
        s3_path: string;
        invoice_id: string;
        data: Invoice;
    }[];
}

export interface ClientDataRender {
    name: string;
    total: number;
}

export interface ClientListGetProps {
    perPage: number;
    pageNumber: number;
}

export interface Client {
    client_id: string;
    client_name: string;
    street_number: number;
    street_address: string;
    zipcode: number;
    city: string;
    country: string;
}

export interface CreateClient {
    client_name: string;
    street_number: number;
    street_address: string;
    zipcode: number;
    city: string;
    country: string;
}

export interface GetClientsResponse {
    per_page: number;
    total: number;
    data: [Client];
}
