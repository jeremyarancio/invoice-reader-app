import {
    CURRENCIES,
    type CreateInvoicePayload,
    type GetInvoice,
    type Invoice,
    type InvoiceData,
    type InvoicePayload,
    type UpdateInvoice,
} from "@/schemas/invoice";
import { toDate } from "@/lib/utils";

export function mapGetInvoiceToInvoice(getInvoice: GetInvoice): Invoice {
    return {
        id: getInvoice.invoice_id,
        clientId: getInvoice.client_id,
        grossAmount: getInvoice.data.gross_amount,
        invoiceNumber: getInvoice.data.invoice_number,
        vat: getInvoice.data.vat,
        issuedDate: new Date(getInvoice.data.issued_date),
        paidDate: getInvoice.data.paid_date ? new Date(getInvoice.data.paid_date) : undefined,
        description: getInvoice.data.description,
        currency: CURRENCIES[getInvoice.data.currency as keyof typeof CURRENCIES]?.symbol || getInvoice.data.currency,
    };
}

export function mapInvoiceDataToPayload(invoiceData: InvoiceData): InvoicePayload {
    return {
        gross_amount: invoiceData.grossAmount,
        invoice_number: invoiceData.invoiceNumber,
        issued_date: toDate(invoiceData.issuedDate),
        paid_date: invoiceData.paidDate ? toDate(invoiceData.paidDate) : undefined,
        vat: invoiceData.vat,
        description: invoiceData.description,
        currency: Object.entries(CURRENCIES).find(
            ([, value]) => value.symbol === invoiceData.currency
        )?.[0] || "usd",
    };
}

export function mapInvoiceToUpdateInvoice(invoiceId: string, invoiceData: InvoiceData): { invoice_id: string; data: UpdateInvoice } {
    return {
        invoice_id: invoiceId,
        data: {
            client_id: "", // This will be set by the hook
            data: mapInvoiceDataToPayload(invoiceData),
        },
    };
}

export function mapInvoiceDataToCreateInvoice(invoiceData: InvoiceData, clientId: string): CreateInvoicePayload {
    return {
        data: mapInvoiceDataToPayload(invoiceData),
        client_id: clientId,
    };
}
