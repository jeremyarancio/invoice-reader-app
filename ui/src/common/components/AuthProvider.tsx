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
    // Token undefined if not logged, null if permission denied
    const [token, setToken] = useState<TokenType>();

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
                if (error.response?.status === 403) {
                    console.log("403 Forbidden detected, clearing token");
                    setToken(null); // Permission denied
                }
                return Promise.reject(error); // Important: re-throw the error
            }
        );

        return () => {
            api.interceptors.response.eject(refreshInterceptor);
        };
    }, []);

    return (
        <AuthContext.Provider value={{ token, setToken }}>
            {children}
        </AuthContext.Provider>
    );
};

export default AuthProvider;
