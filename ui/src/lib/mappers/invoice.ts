import {
    CURRENCIES,
    type CreateInvoicePayload,
    type GetInvoice,
    type Invoice,
    type UpdateInvoice,
} from "@/schemas/invoice";
import { toDate } from "@/lib/utils";

export function mapGetInvoiceToInvoice(getInvoice: GetInvoice): Invoice {
    return {
        id: getInvoice.invoice_id,
        grossAmount: getInvoice.data.gross_amount,
        invoiceNumber: getInvoice.data.invoice_number,
        vat: getInvoice.data.vat,
        issuedDate: getInvoice.data.issued_date,
        paidDate: getInvoice.data.paid_date,
        description: getInvoice.data.description,
        currency:
            CURRENCIES[getInvoice.data.currency as keyof typeof CURRENCIES],
        clientId: getInvoice.client_id,
    };
}

export function mapInvoiceToUpdateInvoice(invoice: Invoice): UpdateInvoice {
    return {
        client_id: invoice.clientId,
        data: {
            gross_amount: invoice.grossAmount,
            invoice_number: invoice.invoiceNumber,
            issued_date: toDate(invoice.issuedDate),
            paid_date: invoice.paidDate ? toDate(invoice.paidDate) : undefined,
            vat: invoice.vat,
            description: invoice.description,
            currency:
                Object.entries(CURRENCIES).find(
                    ([, value]) => value === invoice.currency
                )?.[0] || "usd",
        },
    };
}

export function mapInvoicetoCreateInvoice(
    invoice: Omit<Invoice, "id">
): CreateInvoicePayload {
    return {
        data: {
            gross_amount: invoice.grossAmount,
            invoice_number: invoice.invoiceNumber,
            issued_date: toDate(invoice.issuedDate),
            vat: invoice.vat,
            paid_date: invoice.paidDate ? toDate(invoice.paidDate) : undefined,
            description: invoice.description,
            currency: invoice.currency,
        },
        client_id: invoice.clientId,
    };
}
