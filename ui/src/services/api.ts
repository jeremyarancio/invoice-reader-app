import axios from "axios";
import {
    UserRegistrationData,
    UserLoginData,
    CreateClient,
    GetInvoiceResponse,
} from "../types";
import { QueryClient } from "@tanstack/react-query";
import {
    GetPagedInvoices,
    CreateInvoicePayload,
    UpdateInvoice,
} from "@/pages/invoices/types";
import { GetPagedClients } from "@/pages/clients/types";

const baseURL = "http://localhost:8000/api/v1/";

export const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            refetchOnWindowFocus: false,
            retry: false,
            staleTime: 30000,
        },
        mutations: {
            retry: false,
        },
    },
});

const api = axios.create({
    baseURL: baseURL,
});

export const registerUser = async (userData: UserRegistrationData) => {
    const response = await api.post("users/register/", userData);
    return response.data;
};

export const loginUser = async (loginData: UserLoginData) => {
    const formData = new FormData();
    formData.append("username", loginData.email);
    formData.append("password", loginData.password);
    const response = await api.post("users/login/", formData);
    return response.data;
};

export const submitInvoice = async (file: File, data: CreateInvoicePayload) => {
    const invoiceData = JSON.stringify(data);

    const formData = new FormData();
    formData.append("upload_file", file);
    formData.append("data", invoiceData);

    const accessToken = localStorage.getItem("accessToken");
    const tokenType = localStorage.getItem("tokenType") || "Bearer";

    if (!accessToken) {
        throw new Error("No authentication token found. Please log in.");
    }

    const response = await api.post("invoices/submit/", formData, {
        headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `${tokenType} ${accessToken}`,
        },
    });

    return response.data;
};

export const fetchInvoice = async (id: string): Promise<GetInvoiceResponse> => {
    const accessToken = localStorage.getItem("accessToken");
    const tokenType = localStorage.getItem("tokenType") || "Bearer";

    const response = await api.get("invoices/" + id, {
        headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `${tokenType} ${accessToken}`,
        },
    });
    return response.data;
};

export const fetchInvoices = async (
    pageNumber: number,
    perPage: number
): Promise<GetPagedInvoices> => {
    const accessToken = localStorage.getItem("accessToken");
    const tokenType = localStorage.getItem("tokenType") || "Bearer";

    const response = await api.get("invoices/", {
        params: {
            page: pageNumber,
            per_page: perPage,
        },
        headers: {
            "Content-Type": "application/json",
            Authorization: `${tokenType} ${accessToken}`,
        },
    });
    return response.data;
};

export const fetchClients = async (
    pageNumber: number,
    perPage: number
): Promise<GetPagedClients> => {
    const accessToken = localStorage.getItem("accessToken");
    const tokenType = localStorage.getItem("tokenType") || "Bearer";

    const response = await api.get("clients/", {
        params: {
            page: pageNumber,
            per_page: perPage,
        },
        headers: {
            "Content-Type": "application/json",
            Authorization: `${tokenType} ${accessToken}`,
        },
    });
    return response.data;
};

export const addClient = async (client: CreateClient) => {
    const accessToken = localStorage.getItem("accessToken");
    const tokenType = localStorage.getItem("tokenType") || "Bearer";

    if (!accessToken) {
        throw new Error("No authentication token found. Please log in.");
    }

    const response = await api.post("/clients/add/", client, {
        headers: {
            "Content-Type": "application/json",
            Authorization: `${tokenType} ${accessToken}`,
        },
    });

    return response.data;
};

export const deleteInvoices = async (invoice_ids: string[]) => {
    const accessToken = localStorage.getItem("accessToken");
    const tokenType = localStorage.getItem("tokenType") || "Bearer";

    if (!accessToken) {
        throw new Error("No authentication token found. Please log in.");
    }
    await Promise.all(
        invoice_ids.map(async (invoice_id) => {
            await api.delete("invoices/" + invoice_id, {
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `${tokenType} ${accessToken}`,
                },
            });
        })
    );
};

export const deleteClients = async (client_ids: string[]) => {
    const accessToken = localStorage.getItem("accessToken");
    const tokenType = localStorage.getItem("tokenType") || "Bearer";

    if (!accessToken) {
        throw new Error("No authentication token found. Please log in.");
    }

    await Promise.all(
        client_ids.map(async (client_id) => {
            await api.delete("clients/" + client_id, {
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `${tokenType} ${accessToken}`,
                },
            });
        })
    );
};

export const updateInvoice = async (invoice: UpdateInvoice) => {
    const accessToken = localStorage.getItem("accessToken");
    const tokenType = localStorage.getItem("tokenType") || "Bearer";

    if (!accessToken) {
        throw new Error("No authentication token found. Please log in.");
    }

    const response = await api.put("invoices/" + invoice.id, invoice.invoice, {
        headers: {
            "Content-Type": "application/json",
            Authorization: `${tokenType} ${accessToken}`,
        },
    });

    return response.data;
};

export const fetchInvoiceUrl = async (id: string): Promise<string> => {
    const accessToken = localStorage.getItem("accessToken");
    const tokenType = localStorage.getItem("tokenType") || "Bearer";

    if (!accessToken) {
        throw new Error("No authentication token found. Please log in.");
    }

    const response = await api.get("invoices/" + id + "/url", {
        headers: {
            "Content-Type": "application/json",
            Authorization: `${tokenType} ${accessToken}`,
        },
    });

    return response.data;
};
