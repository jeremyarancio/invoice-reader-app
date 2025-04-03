import { ReactNode } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthProvider";

const ProtectedRoute = ({ children }: { children: ReactNode }) => {
    const { token } = useAuth();

    return token ? children : <Navigate to={"/signin"} replace />;
};

export default ProtectedRoute;
