export const CURRENCIES = {
    usd: { symbol: "$", name: "US Dollar" },
    eur: { symbol: "€", name: "Euro" },
    gbp: { symbol: "£", name: "British Pound" },
} as const;

export type InvoiceData = {
    grossAmount: number;
    vat: number;
    issuedDate: Date;
    paidDate?: Date;
    invoiceNumber: string;
    description: string;
    currency: string;
};

export type Invoice = {
    id: string;
    clientId: string;
} & InvoiceData;

export type InvoicePayload = {
    gross_amount: number;
    vat: number;
    issued_date: string;
    paid_date?: string;
    invoice_number: string;
    description: string;
    currency: string;
};

export interface GetPagedInvoices {
    page: number;
    per_page: number;
    total: number;
    invoices: GetInvoice[];
}

export interface GetInvoice {
    invoice_id: string;
    client_id: string;
    storage_path: string;
    data: InvoicePayload;
}

export interface CreateInvoicePayload {
    data: InvoicePayload;
    client_id: string;
}

export interface UpdateInvoice {
    data: InvoicePayload;
    client_id: string;
}
