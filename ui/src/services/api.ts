import axios from "axios";
import { QueryClient } from "@tanstack/react-query";
import {
    GetPagedInvoices,
    CreateInvoicePayload,
    UpdateInvoice,
    GetInvoice,
    GetCurrency,
} from "@/pages/invoices/types";
import {
    CreateClient,
    GetPagedClients,
    UpdateClient,
} from "@/pages/clients/types";
import { CreateUser, PostUser } from "@/pages/auth/types";

const baseURL = import.meta.env.VITE_SERVER_API_URL;

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

export const api = axios.create({
    baseURL: baseURL,
});

export const registerUser = async (userData: CreateUser) => {
    const response = await api.post("users/signup/", userData);
    return response.data;
};

export const loginUser = async (loginData: PostUser) => {
    const formData = new FormData();
    formData.append("username", loginData.email);
    formData.append("password", loginData.password);
    const response = await api.post("users/signin/", formData);
    return response.data;
};

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
    const response = await api.get("invoices/" + id, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });
    return response.data;
};

export const fetchInvoices = async (
    pageNumber: number,
    perPage: number
): Promise<GetPagedInvoices> => {
    const response = await api.get("invoices/", {
        params: {
            page: pageNumber,
            per_page: perPage,
        },
        headers: {
            "Content-Type": "application/json",
        },
    });
    return response.data;
};

export const fetchClients = async (
    pageNumber: number,
    perPage: number
): Promise<GetPagedClients> => {
    const response = await api.get("clients/", {
        params: {
            page: pageNumber,
            per_page: perPage,
        },
        headers: {
            "Content-Type": "application/json",
        },
    });
    return response.data;
};

export const addClient = async (client: CreateClient) => {
    const response = await api.post("/clients/", client, {
        headers: {
            "Content-Type": "application/json",
        },
    });

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

export const deleteClients = async (client_ids: string[]) => {
    await Promise.all(
        client_ids.map(async (client_id) => {
            await api.delete("clients/" + client_id, {
                headers: {
                    "Content-Type": "application/json",
                },
            });
        })
    );
};

export const updateClient = async (update_client: UpdateClient) => {
    const response = await api.put(
        "clients/" + update_client.id,
        update_client.client,
        {
            headers: {
                "Content-Type": "application/json",
            },
        }
    );
    return response.data;
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

export const fetchCurrencies = async (): Promise<GetCurrency[]> => {
    const response = await api.get("currencies/", {});
    return response.data;
};

export const fetchRefreshToken = async () => {
    // With credentials to send cookies, containing the refresh token
    const response = await api.get("users/refresh/", { withCredentials: true });
    return response.data;
};

export const signOut = async () => {
    await api.get("users/logout/", { withCredentials: true });
};
