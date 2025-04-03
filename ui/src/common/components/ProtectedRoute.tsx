import { ReactNode } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthProvider";

const ProtectedRoute = ({ children }: { children: ReactNode }) => {
    console.log("ProtectedRoute");

    const { token } = useAuth();
    console.log(token);

    return token ? children : <Navigate to={"/signin"} replace />;
};

export default ProtectedRoute;
