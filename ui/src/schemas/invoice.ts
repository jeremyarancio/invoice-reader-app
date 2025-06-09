export interface GetPagedInvoices {
    page: number;
    per_page: number;
    total: number;
    data: GetInvoice[];
}

export interface GetInvoice {
    data: GetInvoiceItem;
    invoice_id: string;
    client_id: string;
    currency_id: string;
    s3_path: string;
}

export interface GetInvoiceItem {
    amount_excluding_tax: number;
    invoice_number: string;
    invoiced_date: Date;
    vat: number;
    is_paid: boolean;
}

export interface Invoice {
    id: string;
    clientId: string;
    grossAmount: number;
    vat: number;
    status: boolean;
    issuedDate: Date;
    invoiceNumber: string;
    currencyId: string;
}

export interface CreateInvoice {
    amount_excluding_tax: number;
    vat: number;
    invoiced_date: string;
    invoice_number: string;
    is_paid: boolean;
}

export interface CreateInvoicePayload {
    invoice: CreateInvoice;
    client_id: string;
    currency_id: string;
}

export interface UpdateInvoice {
    id: string;
    invoice: {
        amount_excluding_tax: number;
        vat: number;
        invoiced_date: Date;
        invoice_number: string;
        is_paid: boolean;
    };
}

export interface GetCurrency {
    currency_id: string;
    currency: string;
}

export interface Currency {
    id: string;
    name: string;
}
