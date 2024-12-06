import axios from "axios";
import { UserRegistrationData, UserLoginData } from "../types";
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
