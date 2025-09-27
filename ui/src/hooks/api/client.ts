import {
    mapClientToUpdateClient,
    mapGetClientToClient,
} from "@/lib/mappers/client";
import type { Client, CreateClient, UpdateClient } from "@/schemas/client";
import {
    addClient,
    deleteClient,
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
    const clients = data?.clients.map(mapGetClientToClient) || [];

    return { clients, isLoading, error };
};

export const useDeleteClient = () => {
    const deleteMutation = useMutation({
        mutationFn: deleteClient,
        onSuccess: () => {
            window.alert("Successfully deleted");
            queryClient.invalidateQueries({ queryKey: ["clients"] });
        },
        onError: (error: AxiosError) => {
            error.status === 422
                ? window.alert(
                      "No client with this ID exists. Please try again."
                  )
                : window.alert("Error: " + error.message);
        },
    });
    return (clientId: string) => {
        deleteMutation.mutate(clientId);
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
        mutationFn: ({
            client_id,
            data,
        }: {
            client_id: string;
            data: UpdateClient;
        }) => updateClient(client_id, data),
        onSuccess: () => {
            window.alert("Client successfully updated.");
            queryClient.invalidateQueries({ queryKey: ["clients"] });
            queryClient.invalidateQueries({ queryKey: ["client"] });
        },
        onError: (error: AxiosError) => {
            window.alert("Failed to update client: " + error.message);
        },
    });
    return (client: Omit<Client, "totalRevenue" | "nInvoices">) =>
        updateMutation.mutateAsync({
            client_id: client.id,
            data: mapClientToUpdateClient(client),
        });
};
