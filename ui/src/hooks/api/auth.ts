import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { AxiosError } from "axios";
import { useAuth } from "@/components/AuthProvider";
import { signIn, signOut, signUp } from "@/services/api/auth";
import type { PostUser } from "@/schemas/user";
import { queryClient } from "@/services/api/main";

export const useSignIn = () => {
    const { setToken } = useAuth();
    const navigate = useNavigate();

    const signInMutation = useMutation({
        mutationFn: signIn,
        onSuccess: (data) => {
            setToken(data.access_token);
            navigate("/invoices");
        },
        onError: (error: AxiosError) => {
            error.status === 401
                ? window.alert("Invalid credentials")
                : window.alert(error.message);
        },
    });

    return (postUser: PostUser) => {
        signInMutation.mutate(postUser);
    };
};

export const useSignUp = () => {
    const navigate = useNavigate();
    const SignUpMutation = useMutation({
        mutationFn: signUp,
        onSuccess: () => {
            window.alert("User registered successfully. You can sign in!");
            navigate("/signin");
        },
        onError: (error: AxiosError) => {
            error.status === 409
                ? window.alert("User already registered.")
                : window.alert(error.message);
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
