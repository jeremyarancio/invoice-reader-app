export interface InvoiceDataRender {
    invoiceNumber: string;
    clientName: string;
    invoicedDate: Date;
    amountExcludingTax: number;
    vat: number;
    currency: string;
    paid?: boolean;
}

export interface InvoiceData {
    amount_excluding_tax: number;
    vat: number;
    currency: string;
    invoiced_date: Date;
    invoice_number: string;
}

export interface AddInvoicePayload {
    invoice: InvoiceData;
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
        file_id: string;
        s3_path: string;
        data: InvoiceData;
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

export interface ClientData {
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
    data: [ClientData];
}
