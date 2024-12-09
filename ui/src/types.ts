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
    client_name: string;
    amount_excluding_tax: number;
    vat: number;
    currency: string;
    invoiced_date: Date;
    invoice_number: string;
    street_number: number;
    street_address: string;
    zipcode: string;
    city: string;
    country: string;
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

export interface GetInvoiceResponse {
    page: number;
    per_page: number;
    total: number;
    data: {
        file_id: string;
        s3_path: string;
        data: InvoiceData;
    }[];
}
