import type {
    CreateInvoicePayload,
    GetInvoice,
    GetPagedInvoices,
    UpdateInvoice,
} from "@/schemas/invoice";
import type { ParsedInvoice } from "@/schemas/parser";
import { api } from "@/services/api/main";

export const addInvoice = async (file: File, data: CreateInvoicePayload) => {
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

export const deleteInvoice = async (invoiceId: string) => {
    await api.delete("invoices/" + invoiceId);
};

export const updateInvoice = async (invoice_id: string, data: UpdateInvoice) => {
    await api.put("invoices/" + invoice_id, data);
};

export const fetchInvoiceUrl = async (id: string): Promise<string> => {
    const response = await api.get("invoices/" + id + "/url/");
    return response.data;
};
export const parseInvoice = async (file: File): Promise<ParsedInvoice> => {
    const formData = new FormData();
    formData.append("upload_file", file);

    const response = await api.post("invoices/parse/", formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });

    return response.data;
};
