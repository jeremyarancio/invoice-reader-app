import {
    CreateInvoicePayload,
    GetInvoice,
    Invoice,
    UpdateInvoice,
} from "./types";

export function mapGetInvoiceToInvoice(getInvoice: GetInvoice): Invoice {
    return {
        id: getInvoice.invoice_id,
        amountExcludingTax: getInvoice.data.amount_excluding_tax,
        currency: "$", //TODO
        vat: getInvoice.data.vat,
        invoiceNumber: getInvoice.data.invoice_number,
        invoicedDate: getInvoice.data.invoiced_date,
    };
}

export function mapInvoiceToPutInvoice(invoice: Invoice): UpdateInvoice {
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

export function mapInvoicetoCreateInvoice(
    invoice: Omit<Invoice, "id">
): CreateInvoicePayload {
    return {
        invoice: {
            amount_excluding_tax: invoice.amountExcludingTax,
            currency: invoice.currency,
            invoice_number: invoice.invoiceNumber,
            invoiced_date: invoice.invoicedDate,
            vat: invoice.vat,
        },
        client_id: invoice.clientId,
    };
}
