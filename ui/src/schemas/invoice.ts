export const CURRENCIES = {
    "usd": "$",
    "eur": "€",
    "gbp": "£",
}

export interface GetPagedInvoices {
    page: number;
    per_page: number;
    total: number;
    invoices: GetInvoice[];
}

export interface GetInvoice {
    data: GetInvoiceItem;
    invoice_id: string;
    client_id: string;
    storage_path: string;
}

export interface GetInvoiceItem {
    gross_amount: number;
    invoice_number: string;
    issued_date: Date;
    paid_date?: Date;
    description: string;
    vat: number;
    currency: string;
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
    currency: string;
}

export interface CreateInvoicePayload {
    data: {
        gross_amount: number;
        vat: number;
        issued_date: string;
        paid_date?: string;
        invoice_number: string;
        description: string;
        currency: string;
    };
    client_id: string;
}

export interface UpdateInvoice {
    client_id: string;
    data: {
        gross_amount: number;
        vat: number;
        issued_date: string;
        paid_date?: string;
        invoice_number: string;
        description: string;
        currency: string;
    };
}
