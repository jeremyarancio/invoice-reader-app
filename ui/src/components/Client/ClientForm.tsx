import React, { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { Form, Button, Alert } from "react-bootstrap";
import { addClient } from "../../services/api";
import { CreateClient } from "../../types";
import { useNavigate } from "react-router-dom";

const INITIAL_FORM_STATE: CreateClient = {
    client_name: "",
    street_number: 0,
    street_address: "",
    zipcode: 0,
    city: "",
    country: "",
};

const ClientForm = () => {
    const [formData, setFormData] = useState<CreateClient>(INITIAL_FORM_STATE);
    const [error, setError] = useState<string | null>(null);
    const [isComplete, setIsComplete] = useState<boolean>(false);
    const navigate = useNavigate();

    const ClientDataMutation = useMutation({
        mutationFn: ({ data }: { data: CreateClient }) => {
            return addClient(data);
        },
        onSuccess: () => {
            setFormData(INITIAL_FORM_STATE);
            setError(null);
            setIsComplete(true);
        },
        onError: (error: Error) => {
            setError(error.message || "Failed to submit invoice data");
            console.error(error);
        },
    });

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;

        const processedValue = ["zipcode", "street_number"].includes(name)
            ? Number(value)
            : value;

        setFormData((prev) => ({
            ...prev,
            [name]: processedValue,
        }));
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        error && <Alert>{error}</Alert>;

        try {
            ClientDataMutation.mutate({ data: formData });
        } catch (err) {
            setError(
                err instanceof Error
                    ? err.message
                    : "An unexpected error occurred"
            );
        }
    };

    return (
        <>
            {error && (
                <Alert
                    variant="danger"
                    onClose={() => setError(null)} // Allow dismissing the error
                    dismissible
                    className="mb-4"
                >
                    {error}
                </Alert>
            )}
            {isComplete && (
                <Alert
                    variant="success"
                    dismissible
                    onClose={() => navigate("/")}
                    className="mb-4"
                >
                    Client successfully added
                </Alert>
            )}
            <Form onSubmit={handleSubmit}>
                <h3>Client details</h3>
                <Form.Group className="mb-3">
                    <Form.Label>Client name</Form.Label>
                    <Form.Control
                        type="text"
                        name="client_name"
                        value={formData.client_name}
                        onChange={handleInputChange}
                        required
                    />
                </Form.Group>

                <Form.Group className="mb-3">
                    <Form.Label>Street Number</Form.Label>
                    <Form.Control
                        type="number"
                        name="street_number"
                        value={formData.street_number}
                        onChange={handleInputChange}
                        required
                    />
                </Form.Group>

                <Form.Group className="mb-3">
                    <Form.Label>Street Address</Form.Label>
                    <Form.Control
                        type="text"
                        name="street_address"
                        value={formData.street_address}
                        onChange={handleInputChange}
                        required
                    />
                </Form.Group>

                <Form.Group className="mb-3">
                    <Form.Label>Zipcode</Form.Label>
                    <Form.Control
                        type="text"
                        name="zipcode"
                        value={formData.zipcode}
                        onChange={handleInputChange}
                        required
                    />
                </Form.Group>

                <Form.Group className="mb-3">
                    <Form.Label>City</Form.Label>
                    <Form.Control
                        type="text"
                        name="city"
                        value={formData.city}
                        onChange={handleInputChange}
                        required
                    />
                </Form.Group>

                <Form.Group className="mb-3">
                    <Form.Label>Country</Form.Label>
                    <Form.Control
                        type="text"
                        name="country"
                        value={formData.country}
                        onChange={handleInputChange}
                        required
                    />
                </Form.Group>

                <div className="text-center mt-3">
                    <Button variant="primary" type="submit">
                        Submit
                    </Button>
                </div>
            </Form>
        </>
    );
};

export default ClientForm;
