import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { AxiosError } from "axios";
import { useAuth } from "@/contexts/AuthProvider";
import { signIn, signOut, signUp } from "@/services/api/auth";
import type { PostUser } from "@/schemas/user";
import { queryClient } from "@/services/api/main";
import { useAlert } from "@/contexts/AlertContext";

export const useSignIn = () => {
    const { setToken } = useAuth();
    const navigate = useNavigate();
    const { showAlert } = useAlert();

    const signInMutation = useMutation({
        mutationFn: signIn,
        onSuccess: (data) => {
            setToken(data.access_token);
            navigate("/invoices");
        },
        onError: (error: AxiosError) => {
            let message: string;

            if (error.status === 401) {
                message = "Invalid credentials.";
            } else if (error.status === 404) {
                message =
                    "There is no user with this email. Are you sure you registered?";
            } else {
                message = "Something went wrong.";
            }

            showAlert("error", "Login Failed", message);
        },
    });

    return (postUser: PostUser) => {
        signInMutation.mutate(postUser);
    };
};

export const useSignUp = () => {
    const navigate = useNavigate();
    const { showAlert } = useAlert();

    const SignUpMutation = useMutation({
        mutationFn: signUp,
        onSuccess: () => {
            showAlert(
                "success",
                "Success!",
                "User registered successfully. You can sign in!"
            );
            navigate("/signin");
        },
        onError: (error: AxiosError) => {
            const message =
                error.status === 409
                    ? "User already registered."
                    : error.message;

            showAlert("error", "Registration Failed", message);
        },
    });

    return (postUser: PostUser) => {
        SignUpMutation.mutate(postUser);
    };
};

export const useSignOut = () => {
    const { setToken } = useAuth();
    return async () => {
        queryClient.clear();
        await signOut();
        setToken(null);
    };
};
