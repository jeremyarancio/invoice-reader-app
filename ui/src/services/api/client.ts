import type {
    CreateClient,
    GetClient,
    GetPagedClients,
    UpdateClient,
} from "@/schemas/client";
import { api } from "@/services/api/main";

export const fetchClient = async (id: string): Promise<GetClient> => {
    const response = await api.get("clients/" + id);
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

export const deleteClient = async (clientId: string) => {
    await api.delete("clients/" + clientId);
};

export const updateClient = async (client_id: string, update_client: UpdateClient) => {
    const response = await api.put(
        "clients/" + client_id,
        update_client,
        {
            headers: {
                "Content-Type": "application/json",
            },
        }
    );
    return response.data;
};
