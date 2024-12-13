import React, { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { Form, Button, Row, Col, Alert } from "react-bootstrap";
import { submitInvoice } from "../../services/api";
import { InvoiceData } from "../../types";

interface FormProperties {
    file: File;
}

const INITIAL_FORM_STATE: InvoiceData = {
    client_name: "",
    amount_excluding_tax: 0,
    vat: 20,
    currency: "€",
    invoiced_date: new Date(),
    invoice_number: "",
    street_number: 0,
    street_address: "",
    zipcode: "",
    city: "",
    country: "",
};

function InvoiceDataForm({ file }: FormProperties) {
    const [formData, setFormData] = useState<InvoiceData>(INITIAL_FORM_STATE);
    const [error, setError] = useState<string | null>(null);

    const invoiceDataMutation = useMutation({
        mutationFn: ({ file, data }: { file?: File; data: InvoiceData }) => {
            if (!file) {
                throw new Error("No valid file provided");
            }
            return submitInvoice(file, data);
        },
        onSuccess: () => {
            setFormData(INITIAL_FORM_STATE);
            setError(null);
        },
        onError: (error: Error) => {
            setError(error.message || "Failed to submit invoice data");
            console.error(error);
        },
    });

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;

        const processedValue = [
            "amount_excluding_tax",
            "vat",
            "street_number",
        ].includes(name)
            ? Number(value)
            : value;

        setFormData((prev) => ({
            ...prev,
            [name]: processedValue,
        }));
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (!file) {
            setError("Please upload an invoice file");
            return;
        }

        error && <Alert>{error}</Alert>;

        try {
            console.log(file, formData);
            invoiceDataMutation.mutate({ file, data: formData });
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
            <Form onSubmit={handleSubmit}>
                <Row>
                    <Col md={6}>
                        <h3>Invoice details</h3>
                        <Form.Group className="mb-3">
                            <Form.Label>Invoice number</Form.Label>
                            <Form.Control
                                type="text"
                                name="invoice_number"
                                value={formData.invoice_number}
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
                    </Col>

                    <Col md={6}>
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
                    </Col>
                </Row>

                <div className="text-center mt-3">
                    <Button variant="primary" type="submit">
                        Submit
                    </Button>
                </div>
            </Form>
        </>
    );
}

export default InvoiceDataForm;
