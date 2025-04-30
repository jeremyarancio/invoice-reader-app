import { useMutation, useQuery } from "@tanstack/react-query";
import {
    addClient,
    deleteClients,
    fetchClients,
    queryClient,
    updateClient,
} from "@/services/api";
import { useNavigate } from "react-router-dom";
import { Client, CreateClient } from "./types";
import { AxiosError } from "axios";
import { mapClientToUpdateClient } from "./mapper";

export const useAddClient = () => {
    const navigate = useNavigate();
    return () => {
        navigate("/clientform");
    };
};

export const useFetchClients = () => {
    return (pageNumber: number = 1, perPage: number = 10) =>
        useQuery({
            queryKey: ["clients", pageNumber, perPage],
            queryFn: () => fetchClients(pageNumber, perPage),
        });
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

export const useSubmitClient = () => {
    const submitMutation = useMutation({
        mutationFn: addClient,
        onSuccess: () => {
            window.alert("Client successfully added.");
            queryClient.invalidateQueries({ queryKey: ["clients"] });
        },
        onError: (error: AxiosError) => {
            window.alert("Failed to add client: " + error.message);
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
