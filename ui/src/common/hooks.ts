import { useAuth } from "@/common/components/AuthProvider";

export const useSignOut = () => {
    const { setToken } = useAuth();
    return () => {
        setToken(undefined); // undefined = Log out
    };
};
