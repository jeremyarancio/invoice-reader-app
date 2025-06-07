import type {
    CreateInvoicePayload,
    GetCurrency,
    GetInvoice,
    GetPagedInvoices,
    UpdateInvoice,
} from "@/schemas/invoice";
import { api } from "@/services/api/main";

export const submitInvoice = async (file: File, data: CreateInvoicePayload) => {
    const invoiceData = JSON.stringify(data);

    const formData = new FormData();
    formData.append("upload_file", file);
    formData.append("data", invoiceData);

    const response = await api.post("invoices/", formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });

    return response.data;
};

export const fetchInvoice = async (id: string): Promise<GetInvoice> => {
    const response = await api.get("invoices/" + id);
    return response.data;
};

export const fetchInvoices = async (
    pageNumber: number,
    perPage: number
): Promise<GetPagedInvoices> => {
    const response = await api.get("invoices/", {
        params: { page: pageNumber, per_page: perPage },
    });
    return response.data;
};

export const fetchCurrencies = async (): Promise<GetCurrency[]> => {
    const response = await api.get("currencies/", {});
    return response.data;
};

export const deleteInvoices = async (invoice_ids: string[]) => {
    await Promise.all(
        invoice_ids.map(async (invoice_id) => {
            await api.delete("invoices/" + invoice_id, {
                headers: {
                    "Content-Type": "application/json",
                },
            });
        })
    );
};

export const updateInvoice = async (invoice: UpdateInvoice) => {
    const response = await api.put("invoices/" + invoice.id, invoice.invoice, {
        headers: {
            "Content-Type": "application/json",
        },
    });

    return response.data;
};

export const fetchInvoiceUrl = async (id: string): Promise<string> => {
    const response = await api.get("invoices/" + id + "/url/", {
        headers: {
            "Content-Type": "application/json",
        },
    });

    return response.data;
};
