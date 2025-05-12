import React, {
    createContext,
    useContext,
    useLayoutEffect,
    useState,
    ReactNode,
} from "react";
import { api, fetchRefreshToken, signOut } from "@/services/api";

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
    localStorage.setItem("token", token || "");

    useLayoutEffect(() => {
        console.log("Token set to:", token);
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
                const originalRequest = error.config;

                if (error.response?.status === 403 && !originalRequest._retry) {
                    console.log("Token expired, refreshing...");
                    originalRequest._retry = true;
                    try {
                        const data = await fetchRefreshToken();
                        console.log("New token received:", data.access_token);
                        setToken(data.access_token);
                        originalRequest.headers.Authorization = `Bearer ${data.access_token}`;
                        return api(originalRequest);
                    } catch (refreshError) {
                        await signOut();
                        return Promise.reject(refreshError);
                    }
                }
                return Promise.reject(error);
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
