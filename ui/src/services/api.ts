import axios from "axios";
import {
    UserRegistrationData,
    UserLoginData,
    InvoiceData,
    InvoiceListGetProps,
    ClientListGetProps,
    ClientData,
} from "../types";
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
    formData.append("username", loginData.email);
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

export const getAllInvoice = async (props: InvoiceListGetProps) => {
    const accessToken = sessionStorage.getItem("accessToken");
    const tokenType = sessionStorage.getItem("tokenType") || "Bearer";

    const response = await api.get("/files/", {
        data: {
            page: props.pageNumber,
            per_page: props.perPage,
        },
        headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `${tokenType} ${accessToken}`,
        },
    });
    console.log(response.data);
    return response.data;
};

export const getAllClient = async (props: ClientListGetProps) => {
    const accessToken = sessionStorage.getItem("accessToken");
    const tokenType = sessionStorage.getItem("tokenType") || "Bearer";

    const response = await api.get("/clients/", {
        data: {
            page: props.pageNumber,
            per_page: props.perPage,
        },
        headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `${tokenType} ${accessToken}`,
        },
    });
    console.log(response.data);
    return response.data;
};

export const addClient = async (data: ClientData) => {
    const clientData = JSON.stringify(data);
    const accessToken = sessionStorage.getItem("accessToken");
    const tokenType = sessionStorage.getItem("tokenType") || "Bearer";

    if (!accessToken) {
        throw new Error("No authentication token found. Please log in.");
    }

    const response = await api.post(
        "/clients/add/",
        JSON.parse(clientData), // Parse the stringified data back to an object
        {
            headers: {
                "Content-Type": "application/json",
                Authorization: `${tokenType} ${accessToken}`,
            },
        }
    );

    return response.data;
};