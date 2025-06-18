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
    gross_amount: number;
    invoice_number: string;
    invoiced_date: Date;
    paid_date?: Date;
    description: string;
    vat: number;
}

export interface Invoice {
    id: string;
    grossAmount: number;
    vat: number;
    issuedDate: Date;
    paidDate?: Date;
    description: string;
    invoiceNumber: string;
    clientId: string;
    currencyId: string;
}

export interface CreateInvoice {
    gross_amount: number;
    vat: number;
    invoiced_date: string;
    paid_date?: string;
    invoice_number: string;
    description: string;
}

export interface CreateInvoicePayload {
    invoice: CreateInvoice;
    client_id: string;
    currency_id: string;
}

export interface UpdateInvoice {
    id: string;
    invoice: {
        gross_amount: number;
        vat: number;
        invoiced_date: string;
        paid_date?: string;
        invoice_number: string;
        description: string;
        currency_id: string;
        client_id: string;
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
