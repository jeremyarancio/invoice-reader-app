import { useState } from "react";
import { Form, Button } from "react-bootstrap";
import InvoiceForm from "./InvoiceForm";
import AlertError from "@/common/components/AlertError";

const UploadInvoice = () => {
    const [file, setFile] = useState<File | null>(null);
    const [error, setError] = useState<Error | null>(null);
    const [showForm, setShowForm] = useState(false);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
        }
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (!file) {
            setError(new Error("File is missing."));
            return;
        }

        setShowForm(true);
    };

    if (showForm && file) {
        return <InvoiceForm file={file} />;
    }

    return (
        <>
            {error && (
                <AlertError error={error} onClose={() => setError(null)} />
            )}
            <h2>Upload Invoice</h2>
            <Form onSubmit={handleSubmit}>
                <Form.Group controlId="formFile" className="mb-3">
                    <Form.Label>Select Invoice PDF</Form.Label>
                    <Form.Control
                        type="file"
                        accept="application/pdf"
                        onChange={handleFileChange}
                    />
                </Form.Group>
                <Button variant="primary" type="submit" disabled={!file}>
                    Next
                </Button>
            </Form>
        </>
    );
};

export default UploadInvoice;
