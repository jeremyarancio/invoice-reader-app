import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";

const Profile = () => {
    const [name, setName] = useState("John Doe");
    const [email, setEmail] = useState("john@example.com");

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        alert(`Profile updated: ${name}, ${email}`);
    };

    return (
        <div>
            <h2>Profile</h2>
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                    <Form.Label>Name</Form.Label>
                    <Form.Control
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                    />
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Email</Form.Label>
                    <Form.Control
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </Form.Group>
                <Button variant="primary" type="submit">
                    Update Profile
                </Button>
            </Form>
        </div>
    );
};

export default Profile;
