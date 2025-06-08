import { QueryClient } from "@tanstack/react-query";
import axios from "axios";

const baseURL = import.meta.env.VITE_SERVER_API_URL;

export const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            refetchOnWindowFocus: false,
            retry: false,
            staleTime: 1000 * 60 * 5,
        },
        mutations: {
            retry: false,
        },
    },
});

export const api = axios.create({
    baseURL: baseURL,
    withCredentials: true, //for cookie
});
