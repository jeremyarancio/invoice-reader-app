import { mapGetClientToClient } from "@/lib/mappers/client";
import { fetchClients } from "@/services/api/client";
import { useQuery } from "@tanstack/react-query";

export const useFetchClients = () => {
    return (pageNumber: number = 1, perPage: number = 10) => {
        const { data, isLoading, error } = useQuery({
            queryKey: ["clients", pageNumber, perPage],
            queryFn: () => fetchClients(pageNumber, perPage),
        });
        const clients = data?.data.map(mapGetClientToClient) || [];

        return { clients, isLoading, error };
    };
};
