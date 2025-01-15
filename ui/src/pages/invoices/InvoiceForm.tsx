import { Invoice } from "./types";
import { useFetchClients } from "../clients/hooks";
import { useSubmitInvoice } from "./hooks";
import SubmissionForm from "../../common/components/SubmissionForm";
import { mapGetClientToClient } from "../clients/mapper";
import { mapInvoicetoCreateInvoice } from "./mappers";
import { Alert } from "react-bootstrap";

type InvoiceFormData = Omit<Invoice, "id">;

interface FormProperties {
    file: File;
}

const initialInvoice: InvoiceFormData = {
    amountExcludingTax: 0,
    vat: 0,
    currency: "€",
    invoicedDate: new Date(),
    invoiceNumber: "",
    clientId: "",
};

function InvoiceForm({ file }: FormProperties) {
    const fetchClients = useFetchClients();
    const submitInvoice = useSubmitInvoice();

    const { data: pagedClients, error } = fetchClients();
    const clients = pagedClients?.data.map(mapGetClientToClient) || [];

    const formGroups = [
        {
            header: "Invoice number",
            key: "invoiceNumber",
            formType: "text" as const, //Literal (lol typescript)
            required: true,
        },
        {
            header: "Amount Excuding Tax",
            key: "amountExcludingTax",
            formType: "number" as const,
            required: true,
        },
        {
            header: "Currency",
            key: "currency",
            formType: "text" as const,
            required: true,
        },
        {
            header: "VAT (%)",
            key: "vat",
            formType: "number" as const,
            required: true,
        },
        {
            header: "invoicedDate",
            key: "invoicedDate",
            formType: "date" as const,
            required: true,
        },
        {
            header: "Client",
            key: "clientId",
            formType: "select" as const,
            required: true,
        },
    ];

    return (
        <>
            {error && <Alert variant="warning">Error: {error.message}</Alert>}
            <SubmissionForm<InvoiceFormData>
                name="Invoice"
                submit={(data: InvoiceFormData) =>
                    submitInvoice(file, mapInvoicetoCreateInvoice(data))
                }
                formGroups={formGroups}
                initialData={initialInvoice}
                additionalItems={clients}
            />
        </>
    );
}

export default InvoiceForm;
