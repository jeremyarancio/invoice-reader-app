import { useMutation, useQuery } from "@tanstack/react-query";
import { deleteClients, fetchClients, queryClient } from "../../services/api";
import { useNavigate } from "react-router-dom";
import { Client } from "./types";

export const useAddClient = () => {
    const navigate = useNavigate();
    return () => {
        navigate("/clientform");
    };
};

export const useFetchClients = () => {
    return (pageNumber: number, perPage: number) =>
        useQuery({
            queryKey: ["clients", pageNumber, perPage],
            queryFn: () => fetchClients(pageNumber, perPage),
            enabled: !!sessionStorage.getItem("accessToken"),
        });
};

export const useDeleteClients = () => {
    const deleteMutation = useMutation({
        mutationFn: deleteClients,
        onSuccess: () => {
            window.alert("Successfully deleted");
            queryClient.invalidateQueries({ queryKey: ["clients"] });
        },
        onError: (error) => {
            alert("Failed to delete invoices: " + error.message);
        },
    });
    return (clients: Client[]) => {
        const clientIds = clients.map((client) => client.id);
        deleteMutation.mutate(clientIds);
    };
};

export const useUpdateClient = () => {
    return () => {};
};
