import React from "react";
import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
    const isAuthenticated = !!localStorage.getItem("accessToken");
    return isAuthenticated ? children : <Navigate to="/signin" />;
};

export default ProtectedRoute;
