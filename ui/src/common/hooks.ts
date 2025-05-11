import { useAuth } from "@/common/components/AuthProvider";
import { queryClient, signOut } from "@/services/api";

export const useSignOut = () => {
    const { setToken } = useAuth();
    return async () => {
        queryClient.clear();
        await signOut();
        setToken(undefined); // undefined = Log out
    };
};
