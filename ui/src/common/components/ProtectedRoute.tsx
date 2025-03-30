import { ReactNode, useEffect, useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { validateToken } from "@/services/api";
import { Modal, Button } from "react-bootstrap";

const ProtectedRoute = ({ children }: { children: ReactNode }) => {
    const navigate = useNavigate();
    const token = localStorage.getItem("accessToken");
    const [isValidToken, setIsValidToken] = useState<boolean | null>(null);

    const { mutate, isPending } = useMutation({
        mutationFn: (token: string) => validateToken(token),
        onSuccess: (isValid) => {
            setIsValidToken(isValid);
            if (!isValid) {
            }
        },
        onError: (error) => {
            console.log(error);
            setIsValidToken(false);
        },
        gcTime: 0 // Avoid caching the result leading to passing the protected route 
    });

    const handleCloseModal = () => {
        localStorage.removeItem("accessToken");
        navigate("/signin", { replace: true });
    };

    if (!token) {
        return <Navigate to="/signin" replace />;
    }

    // ISSUE HERE: the validation is cahced leading to the protected being passed even with wrong expired token
    useEffect(() => {
        if (token) {
            mutate(token);
        } else {
            setIsValidToken(false);
        }
    }, [token, mutate]);

    if (isValidToken === null || isPending) {
        return <div>Loading authentication...</div>;
    }

    if (isValidToken === true) {
        return children;
    }

    // Token is invalid - show modal
    return (
        <Modal show={!isValidToken} onHide={handleCloseModal}>
            <Modal.Header closeButton>
                <Modal.Title>Session expired.</Modal.Title>
            </Modal.Header>
            <Modal.Body>Your session has expired. Please sign in...</Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleCloseModal}>
                    Close
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

export default ProtectedRoute;
