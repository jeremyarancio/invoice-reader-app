import type {
    CreateInvoicePayload,
    Currency,
    GetCurrency,
    GetInvoice,
    Invoice,
    UpdateInvoice,
} from "@/schemas/invoice";
import { toDate } from "@/lib/utils";

export function mapGetInvoiceToInvoice(getInvoice: GetInvoice): Invoice {
    return {
        id: getInvoice.invoice_id,
        grossAmount: getInvoice.data.amount_excluding_tax,
        currencyId: getInvoice.currency_id,
        status: getInvoice.data.is_paid,
        vat: getInvoice.data.vat,
        invoiceNumber: getInvoice.data.invoice_number,
        issuedDate: getInvoice.data.invoiced_date,
        clientId: getInvoice.client_id,
    };
}

export function mapInvoiceToPutInvoice(invoice: Invoice): UpdateInvoice {
    return {
        id: invoice.id,
        invoice: {
            amount_excluding_tax: invoice.grossAmount,
            invoice_number: invoice.invoiceNumber,
            invoiced_date: invoice.issuedDate,
            vat: invoice.vat,
            is_paid: invoice.status,
        },
    };
}

export function mapInvoicetoCreateInvoice(
    invoice: Omit<Invoice, "id">
): CreateInvoicePayload {
    return {
        invoice: {
            amount_excluding_tax: invoice.grossAmount,
            invoice_number: invoice.invoiceNumber,
            invoiced_date: toDate(invoice.issuedDate),
            vat: invoice.vat,
            is_paid: invoice.status,
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
