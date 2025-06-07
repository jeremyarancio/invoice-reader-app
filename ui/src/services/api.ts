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

export const fetchRefreshToken = async (): Promise<string> => {
    // With credentials to send cookies, containing the refresh token
    const response = await api.post("users/refresh/");
    return response.data.access_token;
};

export const signOut = async () => {
    await api.post("users/signout/");
};
