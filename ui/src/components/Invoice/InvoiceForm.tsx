import React, { useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { Form, Button, Alert } from "react-bootstrap";
import { submitInvoice, fetchClients } from "../../services/api";
import { Invoice, GetClientsResponse, AddInvoicePayload } from "../../types";
import { useNavigate } from "react-router-dom";

interface FormProperties {
    file: File;
}

const initialInvoicePayload: Invoice = {
    amount_excluding_tax: 0,
    vat: 0,
    currency: "€",
    invoiced_date: new Date(),
    invoice_number: "",
    invoice_id: "",
    client_id: "",
};

function InvoiceForm({ file }: FormProperties) {
    const [clientId, setClientId] = useState<string>("");
    const [invoicePayload, setInvoicePayload] = useState<Invoice>(
        initialInvoicePayload
    );
    const [error, setError] = useState<string | null>(null);
    const [isComplete, setIsComplete] = useState<boolean>(false);
    const navigate = useNavigate();

    const { data: pagedClients, isError } = useQuery<GetClientsResponse, Error>(
        {
            queryKey: ["clients"],
            queryFn: () => fetchClients({ pageNumber: 1, perPage: 100 }),
        }
    );

    const invoiceDataMutation = useMutation({
        mutationFn: ({
            file,
            data,
        }: {
            file?: File;
            data: AddInvoicePayload;
        }) => {
            if (!file) {
                throw new Error("No valid file provided");
            }
            return submitInvoice(file, data);
        },
        onSuccess: () => {
            setClientId("");
            setInvoicePayload(initialInvoicePayload);
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

        const processedValue = ["amount_excluding_tax", "vat"].includes(name)
            ? Number(value)
            : value;

        setInvoicePayload((prev) => ({
            ...prev,
            [name]: processedValue,
        }));
    };

    const handleSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const { value } = e.target;
        setClientId(value);
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (!file) {
            setError("Please upload an invoice file");
            return;
        }

        try {
            invoiceDataMutation.mutate({
                file,
                data: { invoice: invoicePayload, client_id: clientId },
            });
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
                <h3>Invoice details</h3>
                <Form.Group className="mb-3">
                    <Form.Label>Invoice number</Form.Label>
                    <Form.Control
                        type="text"
                        name="invoice_number"
                        onChange={handleInputChange}
                        required
                    />
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Revenue without tax (€)</Form.Label>
                    <Form.Control
                        type="number"
                        name="amount_excluding_tax"
                        onChange={handleInputChange}
                        required
                    />
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>VAT (%)</Form.Label>
                    <Form.Control
                        type="number"
                        name="vat"
                        onChange={handleInputChange}
                        required
                    />
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Invoice date</Form.Label>
                    <Form.Control
                        type="date"
                        name="invoiced_date"
                        onChange={handleInputChange}
                        required
                    />
                </Form.Group>
                <Form.Group>
                    <Form.Select
                        aria-label="Select a client"
                        name="client_name"
                        onChange={handleSelectChange}
                        required
                    >
                        <option value="">Select a client</option>
                        {isError && (
                            <option disabled>Error loading clients</option>
                        )}
                        {pagedClients?.data.map((client) => (
                            <option
                                key={client.client_id}
                                value={client.client_id}
                            >
                                {client.client_name}
                            </option>
                        ))}
                    </Form.Select>
                </Form.Group>

                <div className="text-center mt-3">
                    <Button variant="primary" type="submit">
                        Submit
                    </Button>
                </div>
            </Form>
        </>
    );
}

export default InvoiceForm;
