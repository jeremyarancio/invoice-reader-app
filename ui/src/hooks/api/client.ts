import {
    mapClientToUpdateClient,
    mapGetClientToClient,
} from "@/lib/mappers/client";
import type { ClientData, CreateClient, UpdateClient } from "@/schemas/client";
import {
    addClient,
    deleteClient,
    fetchClient,
    fetchClientRevenue,
    fetchClients,
    updateClient,
} from "@/services/api/client";
import { queryClient } from "@/services/api/main";
import { useMutation, useQuery } from "@tanstack/react-query";
import type { AxiosError } from "axios";
import { useAlert } from "@/contexts/AlertContext";

export const useFetchClient = (clientId: string) => {
    const { data, isLoading, error } = useQuery({
        queryKey: ["client", clientId],
        queryFn: () => fetchClient(clientId),
        enabled: !!clientId,
    });
    const client = data ? mapGetClientToClient(data) : null;
    return {
        client,
        isLoading: isLoading,
        error: error,
    };
};

export const useFetchClients = (
    pageNumber: number = 1,
    perPage: number = 10
) => {
    const { data, isLoading, error } = useQuery({
        queryKey: ["clients", pageNumber, perPage],
        queryFn: async () => {
            const pagedClients = await fetchClients(pageNumber, perPage);
            return pagedClients;
        },
    });
    const clients = data?.clients.map((c) => mapGetClientToClient(c)) || [];
    return { clients, isLoading, error };
};

export const useDeleteClient = () => {
    const { showAlert } = useAlert();

    const deleteMutation = useMutation({
        mutationFn: deleteClient,
        onSuccess: () => {
            showAlert("success", "Deleted!", "Client deleted successfully");
            queryClient.invalidateQueries({ queryKey: ["clients"] });
        },
        onError: (error: AxiosError) => {
            const message =
                error.status === 422
                    ? "No client with this ID exists. Please try again."
                    : error.message;

            showAlert("error", "Error", message);
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
    const { showAlert } = useAlert();

    const submitMutation = useMutation({
        mutationFn: addClient,
        onSuccess: () => {
            showAlert("success", "Success!", "Client successfully added");
            queryClient.invalidateQueries({ queryKey: ["clients"] });
            config?.onSuccess?.();
        },
        onError: (error: AxiosError) => {
            showAlert(
                "error",
                "Error",
                "Failed to add client: " + error.message
            );
            config?.onError?.(error);
        },
    });
    return (client: CreateClient) => submitMutation.mutate(client);
};

export const useUpdateClient = () => {
    const { showAlert } = useAlert();

    const updateMutation = useMutation({
        mutationFn: ({
            client_id,
            data,
        }: {
            client_id: string;
            data: UpdateClient;
        }) => updateClient(client_id, data),
        onSuccess: () => {
            showAlert("success", "Updated!", "Client successfully updated");
            queryClient.invalidateQueries({ queryKey: ["clients"] });
            queryClient.invalidateQueries({ queryKey: ["client"] });
        },
        onError: (error: AxiosError) => {
            if (error.status === 409) {
                showAlert(
                    "error",
                    "Error",
                    "Failed to update client: " +
                        "Client with this name already exists."
                );
            }
        },
    });
    return (clientId: string, clientData: ClientData) =>
        updateMutation.mutateAsync({
            client_id: clientId,
            data: mapClientToUpdateClient(clientData),
        });
};

export const useFetchClientRevenue = (clientId: string) => {
    const { data: clientRevenue, isLoading, error } = useQuery({
        queryKey: ["clientRevenue", clientId],
        queryFn: () => fetchClientRevenue(clientId),
    });
    return {
        clientRevenue,
        isLoading: isLoading,
        error: error,
    };
};
