import type {
    CreateInvoicePayload,
    GetCurrency,
    GetInvoice,
    GetPagedInvoices,
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
    pageNumber?: number,
    perPage?: number
): Promise<GetPagedInvoices> => {
    const params =
        pageNumber && perPage ? { page: pageNumber, per_page: perPage } : {};

    const response = await api.get("invoices/", { params: params });
    return response.data;
};

export const fetchCurrencies = async (): Promise<GetCurrency[]> => {
    const response = await api.get("currencies/", {});
    return response.data;
};
