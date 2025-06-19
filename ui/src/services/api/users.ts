import type { GetUser } from "@/schemas/user";
import { api } from "@/services/api/main";

export const fetchUser = async (): Promise<GetUser> => {
    const response = await api.get("users/me/");
    return response.data;
};
