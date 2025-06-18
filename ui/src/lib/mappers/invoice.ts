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
        grossAmount: getInvoice.data.gross_amount,
        invoiceNumber: getInvoice.data.invoice_number,
        vat: getInvoice.data.vat,
        issuedDate: getInvoice.data.invoiced_date,
        paidDate: getInvoice.data.paid_date,
        description: getInvoice.data.description,
        currencyId: getInvoice.currency_id,
        clientId: getInvoice.client_id,
    };
}

export function mapInvoiceToUpdateInvoice(invoice: Invoice): UpdateInvoice {
    return {
        id: invoice.id,
        invoice: {
            gross_amount: invoice.grossAmount,
            invoice_number: invoice.invoiceNumber,
            invoiced_date: toDate(invoice.issuedDate),
            paid_date: invoice.paidDate ? toDate(invoice.paidDate) : undefined,
            vat: invoice.vat,
            description: invoice.description,
            currency_id: invoice.currencyId,
            client_id: invoice.clientId,
        },
    };
}

export function mapInvoicetoCreateInvoice(
    invoice: Omit<Invoice, "id">
): CreateInvoicePayload {
    return {
        invoice: {
            gross_amount: invoice.grossAmount,
            invoice_number: invoice.invoiceNumber,
            invoiced_date: toDate(invoice.issuedDate),
            vat: invoice.vat,
            paid_date: invoice.paidDate ? toDate(invoice.paidDate) : undefined,
            description: invoice.description,
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
