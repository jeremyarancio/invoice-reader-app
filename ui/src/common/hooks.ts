import { useAuth } from "@/common/components/AuthProvider";
import { queryClient } from "@/services/api";

export const useSignOut = () => {
    const { setToken } = useAuth();
    queryClient.clear();
    return () => {
        setToken(undefined); // undefined = Log out
    };
};
