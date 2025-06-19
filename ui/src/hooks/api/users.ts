import { fetchUser } from "@/services/api/users";
import { useQuery } from "@tanstack/react-query";

export const useFetchUser = () => {
    const { data, error, isLoading } = useQuery({
        queryKey: ["user"],
        queryFn: fetchUser,
    });
    const user = data || null;
    return { user, error, isLoading };
};
