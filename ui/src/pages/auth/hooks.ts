import { loginUser, registerUser } from "@/services/api";
import { PostUser } from "./types";
import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { AxiosError } from "axios";
import { useAuth } from "@/common/components/AuthProvider";

export const useSignIn = () => {
    const { setToken } = useAuth();
    const navigate = useNavigate();

    const signInMutation = useMutation({
        mutationFn: loginUser,
        onSuccess: (data) => {
            console.log(data.access_token);
            setToken(data.access_token);
            navigate("/");
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
        mutationFn: registerUser,
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
