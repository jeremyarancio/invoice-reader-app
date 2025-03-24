import {
    CreateInvoicePayload,
    Currency,
    GetCurrency,
    GetInvoice,
    Invoice,
    UpdateInvoice,
} from "./types";

export function mapGetInvoiceToInvoice(getInvoice: GetInvoice): Invoice {
    return {
        id: getInvoice.invoice_id,
        amountExcludingTax: getInvoice.data.amount_excluding_tax,
        currencyId: getInvoice.currency_id,
        isPaid: getInvoice.data.is_paid,
        vat: getInvoice.data.vat,
        invoiceNumber: getInvoice.data.invoice_number,
        invoicedDate: getInvoice.data.invoiced_date,
        clientId: getInvoice.client_id,
    };
}

export function mapInvoiceToPutInvoice(invoice: Invoice): UpdateInvoice {
    return {
        id: invoice.id,
        invoice: {
            amount_excluding_tax: invoice.amountExcludingTax,
            invoice_number: invoice.invoiceNumber,
            invoiced_date: invoice.invoicedDate,
            vat: invoice.vat,
            is_paid: invoice.isPaid,
        },
    };
}

export function mapInvoicetoCreateInvoice(
    invoice: Omit<Invoice, "id">
): CreateInvoicePayload {
    return {
        invoice: {
            amount_excluding_tax: invoice.amountExcludingTax,
            invoice_number: invoice.invoiceNumber,
            invoiced_date: invoice.invoicedDate,
            vat: invoice.vat,
            is_paid: invoice.isPaid,
        },
        client_id: invoice.clientId,
        currency_id: invoice.currencyId,
    };
}

export function mapGetCurrencyToCurrency(currency: GetCurrency): Currency {
    return {
        id: currency.currency_id,
        name: currency.currency,
    };
}
