import { useState } from "react";
import { Form, Button } from "react-bootstrap";
import InvoiceDataForm from "./InvoiceDataForm";

const UploadInvoice = () => {
    const [file, setFile] = useState<File | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [showForm, setShowForm] = useState(false);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
        }
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (!file) {
            setError("File is missing.");
            return;
        }

        setShowForm(true);
    };

    if (showForm && file) {
        return <InvoiceDataForm file={file} />;
    }

    return (
        <div>
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
        </div>
    );
};

export default UploadInvoice;
