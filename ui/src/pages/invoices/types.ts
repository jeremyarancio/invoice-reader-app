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
    s3_path: string;
}

export interface GetInvoiceItem {
    amount_excluding_tax: number;
    invoice_number: string;
    invoiced_date: Date;
    vat: number;
    is_paid: boolean;
    currency: string;
}

export interface Invoice {
    id: string;
    clientId: string;
    amountExcludingTax: number;
    vat: number;
    currency: string;
    isPaid: boolean;
    invoicedDate: Date;
    invoiceNumber: string;
}

export interface CreateInvoice {
    amount_excluding_tax: number;
    vat: number;
    currency: string;
    invoiced_date: Date;
    invoice_number: string;
}

export interface CreateInvoicePayload {
    invoice: CreateInvoice;
    client_id: string;
}

export interface UpdateInvoice {
    id: string;
    invoice: {
        amount_excluding_tax: number;
        vat: number;
        currency: string;
        invoiced_date: Date;
        invoice_number: string;
        is_paid: boolean;
    };
}
