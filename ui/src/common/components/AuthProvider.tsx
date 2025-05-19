import React, {
    createContext,
    useContext,
    useLayoutEffect,
    useState,
    ReactNode,
} from "react";
import { fetchRefreshToken, api } from "@/services/api";

type TokenType = string | null;

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
    const [token, setToken] = useState<TokenType>(null);
    const [isInitializing, setIsInitializing] = useState(true);

    useLayoutEffect(() => {
        const initializeAuth = async () => {
            try {
                const access_token = await fetchRefreshToken();
                setToken(access_token);
            } catch (error) {
                setToken(null); // Explicitly set to null if no valid refresh token
            } finally {
                setIsInitializing(false);
            }
        };
        initializeAuth();
    }, []);

    useLayoutEffect(() => {
        const authInterceptor = api.interceptors.request.use((config) => {
            if (token && !config.headers.Authorization) {
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        });

        const refreshInterceptor = api.interceptors.response.use(
            (response) => response,
            async (error) => {
                const originalRequest = error.config;
                if (error.response?.status === 403 && !originalRequest._retry) {
                    originalRequest._retry = true;
                    try {
                        const access_token = await fetchRefreshToken();
                        setToken(access_token);
                        const newRequest = {
                            ...originalRequest,
                            headers: {
                                ...originalRequest.headers,
                                Authorization: `Bearer ${access_token}`,
                            },
                        };

                        return api(newRequest);
                    } catch (refreshError) {
                        setToken(null);
                        return Promise.reject(refreshError);
                    }
                }
                return Promise.reject(error);
            }
        );
        return () => {
            api.interceptors.request.eject(authInterceptor);
            api.interceptors.response.eject(refreshInterceptor);
        };
    }, [token]);

    return (
        <AuthContext.Provider value={{ token, setToken }}>
            {!isInitializing && children}
        </AuthContext.Provider>
    );
};

export default AuthProvider;
