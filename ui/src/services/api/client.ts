import type {
    CreateClient,
    GetPagedClients,
    UpdateClient,
} from "@/schemas/client";
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
