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
import { CreateUser, PostUser } from "@/schemas/user";

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


export const fetchRefreshToken = async (): Promise<string> => {
    // With credentials to send cookies, containing the refresh token
    const response = await api.post("users/refresh/");
    return response.data.access_token;
};

export const signOut = async () => {
    await api.post("users/signout/");
};
