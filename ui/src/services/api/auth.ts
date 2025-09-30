import type { CreateUser, PostUser } from "@/schemas/user";
import { api } from "@/services/api/main";

export const signUp = async (userData: CreateUser) => {
    const response = await api.post("users/signup", userData);
    return response.data;
};

export const signIn = async (loginData: PostUser) => {
    const formData = new FormData();
    formData.append("username", loginData.email);
    formData.append("password", loginData.password);
    const response = await api.post("users/signin", formData);
    return response.data;
};

export const signOut = async () => {
    await api.post("users/signout");
};

export const fetchRefreshToken = async (): Promise<string> => {
    const response = await api.post("users/refresh");
    return response.data.access_token;
};
