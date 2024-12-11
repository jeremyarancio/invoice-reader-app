import React, { useState } from "react";
import { Form, Button, Alert } from "react-bootstrap";
import { registerUser } from "../../services/api";
import { useMutation } from "@tanstack/react-query";

const RegisterUser = () => {
    const [userName, setUserName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState<string | null>(null);

    const registrationMutation = useMutation({
        mutationFn: registerUser,
        onSuccess: (data) => {
            console.log("Registration successful", data);
            alert("Registration successful! You can now log in.");
            setEmail("");
            setPassword("");
            setConfirmPassword("");
            setError(null);
        },
        onError: (error: any) => {
            const errorMessage =
                error.response?.data?.message ||
                "Registration failed. Please try again.";
            setError(errorMessage);
            console.log(errorMessage);
        },
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (password !== confirmPassword) {
            alert("Passwords do not match!");
            return;
        }
        setError(null);
        registrationMutation.mutate({
            email: email,
            password: password,
        });
    };

    return (
        <div>
            <h2>Register</h2>
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                    <Form.Label>Email</Form.Label>
                    <Form.Control
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Enter your email"
                    />
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Password</Form.Label>
                    <Form.Control
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Enter your password"
                    />
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Confirm Password</Form.Label>
                    <Form.Control
                        type="password"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        placeholder="Re-enter your password"
                    />
                </Form.Group>
                <Button
                    variant="primary"
                    type="submit"
                    disabled={registrationMutation.isPending}
                    className="w-100"
                >
                    {registrationMutation.isPending
                        ? "Registering..."
                        : "Register"}
                </Button>
            </Form>
            {registrationMutation.isSuccess && (
                <Alert variant="success" className="mt-3">
                    Registration successful! You can now log in.
                </Alert>
            )}
        </div>
    );
};

export default RegisterUser;
