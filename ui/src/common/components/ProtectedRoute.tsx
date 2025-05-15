import { ReactNode } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthProvider";

const ProtectedRoute = ({ children }: { children: ReactNode }) => {
    const { token, isInitializing } = useAuth();

    if (isInitializing) {
        return <div>Loading...</div>;
    }

    if (!token) {
        return <Navigate to="/signin" replace />;
    }

    return children;
};
export default ProtectedRoute;
