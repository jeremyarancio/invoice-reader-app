import { GetInvoice, Invoice, PutInvoice } from "../pages/invoices/types";

export function mapInvoicePayloadToInvoice(payload: GetInvoice): Invoice {
    return {
        id: payload.invoice_id,
        amountExcludingTax: payload.data.amount_excluding_tax,
        currency: "$", //TODO
        vat: payload.data.vat,
        invoiceNumber: payload.data.invoice_number,
        invoicedDate: payload.data.invoiced_date,
    };
}

export function mapInvoiceToPutInvoice(invoice: Invoice): PutInvoice {
    return {
        id: invoice.id,
        invoice: {
            amount_excluding_tax: invoice.amountExcludingTax,
            currency: invoice.currency,
            invoice_number: invoice.invoiceNumber,
            invoiced_date: invoice.invoicedDate,
            vat: invoice.vat,
        },
    };
}
