export interface ParsedInvoice {
    invoice: {
        gross_amount?: number;
        vat?: number;
        issued_date?: string;
        invoice_number?: string;
        invoice_description?: string;
        currency?: string;
    };
    client_id?: string;
}
