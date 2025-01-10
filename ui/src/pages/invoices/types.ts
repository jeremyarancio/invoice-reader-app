export interface GetPagedInvoices {
    page: number;
    per_page: number;
    total: number;
    data: GetInvoice[];
}

export interface GetInvoice {
    data: GetInvoiceItems;
    invoice_id: string;
    s3_path: string;
}

export interface GetInvoiceItems {
    amount_excluding_tax: number;
    invoice_number: string;
    invoiced_date: Date;
    vat: number;
}

export interface Invoice {
    id: string;
    // clientId: string;
    amountExcludingTax: number;
    vat: number;
    currency: string;
    invoicedDate: Date;
    invoiceNumber: string;
}

export interface PostInvoice {
    amount_excluding_tax: number;
    vat: number;
    currency: string;
    invoiced_date: Date;
    invoice_number: string;
}

export interface PostInvoicePayload {
    invoice: PostInvoice;
    client_id: string;
}

export interface PutInvoice {
    id: string,
    invoice: {
        amount_excluding_tax: number;
        vat: number;
        currency: string;
        invoiced_date: Date;
        invoice_number: string;
    };
}
