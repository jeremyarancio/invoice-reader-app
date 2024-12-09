import axios from "axios";
import { UserRegistrationData, UserLoginData, InvoiceData } from "../types";
import { QueryClient } from "@tanstack/react-query";

const baseURL = "http://localhost:8000/api/v1/";

export const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            refetchOnWindowFocus: false,
            retry: 1,
        },
        mutations: {
            retry: 1,
        },
    },
});

const api = axios.create({
    baseURL: baseURL,
});

export const registerUser = async (userData: UserRegistrationData) => {
    const response = await api.post("users/register/", userData);
    console.log(response);
    return response.data;
};

export const loginUser = async (loginData: UserLoginData) => {
    const formData = new FormData();
    formData.append("username", loginData.username);
    formData.append("password", loginData.password);
    const response = await api.post("users/login/", formData);
    return response.data;
};

export const submitInvoice = async (file: File, data: InvoiceData) => {
    const invoiceData = JSON.stringify(data);

    const formData = new FormData();
    formData.append("upload_file", file);
    formData.append("data", invoiceData);

    const accessToken = sessionStorage.getItem("accessToken");
    const tokenType = sessionStorage.getItem("tokenType") || "Bearer";

    if (!accessToken) {
        throw new Error("No authentication token found. Please log in.");
    }

    const response = await api.post("/files/submit/", formData, {
        headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `${tokenType} ${accessToken}`,
        },
    });

    return response.data;
};
