import { useEffect } from "react";
import { api } from "@/services/api/main";
import { useAlert } from "@/contexts/AlertContext";
import type { AxiosError } from "axios";

function ApiErrorHandler() {
    const { showAlert } = useAlert();

    useEffect(() => {
        const interceptor = api.interceptors.response.use(
            (response) => response,
            (error: AxiosError) => {
                const status = error.response?.status;

                console.log(error);

                if (status && status >= 500) {
                    const message =
                        "An unexpected server error occurred. Please try again later.";
                    showAlert("error", "Server Error", message);
                } else if (!status) {
                    console.error("Network error:", error.message, error.code);
                    showAlert(
                        "error",
                        "Connection Error",
                        "Unable to connect to the server. Please check your connection and try again."
                    );
                }

                return Promise.reject(error);
            }
        );

        return () => {
            api.interceptors.response.eject(interceptor);
        };
    }, [showAlert]);

    return null;
}

export default ApiErrorHandler;
