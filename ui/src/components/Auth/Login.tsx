import { useState } from "react";
import { Form, Button } from "react-bootstrap";
import { useMutation } from "@tanstack/react-query";

const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const registrationMutation = useMutation({
        mutationFn: registerUser,
        onSuccess: (data) => {
          console.log("Registration successful", data);
          alert("Registration successful! You can now log in.");
          setUserName("");
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
    };

    return (
        <div>
            <h2>Login</h2>
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                    <Form.Label>Email</Form.Label>
                    <Form.Control
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Password</Form.Label>
                    <Form.Control
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </Form.Group>
                <Button variant="primary" type="submit">
                    Login
                </Button>
            </Form>
        </div>
    );
};

export default Login;
