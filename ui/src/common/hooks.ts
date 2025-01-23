import { useNavigate } from "react-router-dom";

export const useSignOut = () => {
    const navigate = useNavigate();
    return () => {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("tokenType");
        navigate("/signin");
    };
};
