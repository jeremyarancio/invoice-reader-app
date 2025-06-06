import type { CreateClient, GetPagedClients } from "@/schemas/client";
import { api } from "./main";

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
