export interface InvoiceDataRender {
    id: number;
    number: string;
    clientName: string;
    date: string;
    revenue: number;
    paid: boolean;
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
    username: string;
    email: string;
    password: string;
}

export interface UserLoginData {
    username: string;
    password: string;
}
