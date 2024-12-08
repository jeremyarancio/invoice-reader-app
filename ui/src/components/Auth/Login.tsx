import { useState } from "react";
import { Form, Button, Alert } from "react-bootstrap";
import { useMutation } from "@tanstack/react-query";
import { loginUser } from "../../services/api";

const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState<string | null>(null);

    const loginMutation = useMutation({
        mutationFn: loginUser,
        onSuccess: (data) => {
            // localStorage.setItem("accessToken", data.accessToken);
            sessionStorage.setItem("accessToken", data.access_token);
            sessionStorage.setItem("tokenType", data.token_type);
            setEmail("");
            setPassword("");
            setError(null);
        },
        onError: (error: any) => {
            const errorMessage =
                error.response?.data?.message ||
                "Login failed. Please check your credentials.";
            setError(errorMessage);
        },
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (!email || !password) {
            setError("Please enter both email and password");
            return;
        }

        loginMutation.mutate({ username: email, password: password });
    };

    return (
        <div>
            <h2>Login</h2>
            {error && <Alert variant="danger">{error}</Alert>}
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                    <Form.Label>Email</Form.Label>
                    <Form.Control
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Password</Form.Label>
                    <Form.Control
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </Form.Group>
                <Button
                    variant="primary"
                    type="submit"
                    disabled={loginMutation.isPending}
                >
                    {loginMutation.isPending ? "Logging in..." : "Login"}
                </Button>
            </Form>
        </div>
    );
};

export default Login;
