import { useState } from "react";
import { Alert } from "react-bootstrap";
import SubmissionForm from "../../common/components/SubmissionForm";
import { Client } from "./types";
import { useSubmitClient } from "./hooks";
import { mapClientToCreateClient } from "./mapper";

type formClient = Omit<Client, "id">;

const initialClient: formClient = {
    name: "",
    streetNumber: 0,
    streetAddress: "",
    zipcode: 0,
    city: "",
    country: "",
};

const ClientForm = () => {
    const [error, setError] = useState<string | null>(null);
    const submitClient = useSubmitClient();

    const formGroups = [
        {
            header: "Client name",
            key: "name",
            formType: "text" as const,
            required: true,
        },
        {
            header: "Street number",
            key: "streetNumber",
            formType: "number" as const,
            required: true,
        },
        {
            header: "Street address",
            key: "streetAddress",
            formType: "text" as const,
            required: true,
        },
        {
            header: "Zipcode",
            key: "zipcode",
            formType: "number" as const,
            required: true,
        },
        {
            header: "Country",
            key: "country",
            formType: "text" as const,
            required: true,
        },
    ];

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
            <SubmissionForm
                name="Client"
                initialData={initialClient}
                formGroups={formGroups}
                submit={(formClient: formClient) =>
                    submitClient(mapClientToCreateClient(formClient))
                }
            />
        </>
    );
};

export default ClientForm;
