import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "@/components/AuthProvider";

const ProtectedRoute = () => {
    const { token } = useAuth();
    return token ? <Outlet /> : <Navigate to="/signin" replace />;
};
export default ProtectedRoute;
