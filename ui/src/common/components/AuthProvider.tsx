import React, {
    createContext,
    useContext,
    useLayoutEffect,
    useState,
    ReactNode,
} from "react";
import { api } from "@/services/api";

type TokenType = string | null | undefined;

interface AuthContextType {
    token: TokenType;
    setToken: React.Dispatch<TokenType>;
}

export const AuthContext = createContext<AuthContextType | undefined>(
    undefined
);

export const useAuth = () => {
    const authContext = useContext(AuthContext);
    if (!authContext) {
        throw new Error("useAuth must be used within AuthProvider.");
    }
    return authContext;
};

const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [token, setToken] = useState<TokenType>();

    console.log("AuthProvider");
    console.log("AUTH token:", token);

    useLayoutEffect(() => {
        const authInterceptor = api.interceptors.request.use((config) => {
            config.headers.Authorization = token
                ? `Bearer ${token}`
                : config.headers.Authorization;
            return config;
        });

        return () => {
            api.interceptors.request.eject(authInterceptor);
        };
    }, [token]);

    useLayoutEffect(() => {
        const refreshInterceptor = api.interceptors.response.use(
            (response) => response,
            async (error) => {
                error.response.status === 403 && setToken(null);
            }
        );
        return api.interceptors.response.eject(refreshInterceptor);
    });

    return (
        <AuthContext.Provider
            value={{
                token,
                setToken,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};

export default AuthProvider;
