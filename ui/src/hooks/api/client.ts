import {
    mapClientToUpdateClient,
    mapGetClientToClient,
} from "@/lib/mappers/client";
import type { Client, CreateClient } from "@/schemas/client";
import {
    addClient,
    deleteClients,
    fetchClient,
    fetchClients,
    updateClient,
} from "@/services/api/client";
import { queryClient } from "@/services/api/main";
import { useMutation, useQuery } from "@tanstack/react-query";
import type { AxiosError } from "axios";

export const useFetchClient = (clientId: string | undefined) => {
    const { data, isLoading, error } = useQuery({
        queryKey: ["client", clientId],
        queryFn: () => fetchClient(clientId as string),
        enabled: !!clientId,
    });
    const client = data ? mapGetClientToClient(data) : null;
    return { client, isLoading, error };
};

export const useFetchClients = (
    pageNumber: number = 1,
    perPage: number = 10
) => {
    const { data, isLoading, error } = useQuery({
        queryKey: ["clients", pageNumber, perPage],
        queryFn: () => fetchClients(pageNumber, perPage),
    });
    const clients = data?.data.map(mapGetClientToClient) || [];

    return { clients, isLoading, error };
};

export const useDeleteClients = () => {
    const deleteMutation = useMutation({
        mutationFn: deleteClients,
        onSuccess: () => {
            window.alert("Successfully deleted");
            queryClient.invalidateQueries({ queryKey: ["clients"] });
        },
        onError: (error: AxiosError) => {
            error.status === 409
                ? window.alert(
                      "Error: Client already exists. Process cancelled."
                  )
                : window.alert("Error: " + error.message);
        },
    });
    return (clients: Client[]) => {
        const clientIds = clients.map((client) => client.id);
        deleteMutation.mutate(clientIds);
    };
};

export const useAddClient = (config?: {
    onSuccess?: () => void;
    onError?: (error: AxiosError) => void;
}) => {
    const submitMutation = useMutation({
        mutationFn: addClient,
        onSuccess: () => {
            window.alert("Client successfully added.");
            queryClient.invalidateQueries({ queryKey: ["clients"] });
            config?.onSuccess?.();
        },
        onError: (error: AxiosError) => {
            window.alert("Failed to add client: " + error.message);
            config?.onError?.(error);
        },
    });
    return (client: CreateClient) => submitMutation.mutate(client);
};

export const useUpdateClient = () => {
    const updateMutation = useMutation({
        mutationFn: updateClient,
        onSuccess: () => {
            window.alert("Client successfully updated.");
            queryClient.invalidateQueries({ queryKey: ["clients"] });
        },
        onError: (error: AxiosError) => {
            window.alert("Failed to update client: " + error.message);
        },
    });
    return (client: Client) =>
        updateMutation.mutate(mapClientToUpdateClient(client));
};
