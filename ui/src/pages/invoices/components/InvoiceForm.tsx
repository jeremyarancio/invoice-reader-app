import { Invoice } from "../types";
import { useFetchClients } from "../../clients/hooks";
import { useSubmitInvoice } from "../hooks";
import SubmissionForm from "../../../common/components/SubmissionForm";
import { mapGetClientToClient } from "../../clients/mapper";
import { mapInvoicetoCreateInvoice } from "../mappers";
import { Alert, Container } from "react-bootstrap";
import PdfPreview from "../../../common/components/PdfPreview";

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
    isPaid: false,
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
        {
            header: "Paid?",
            key: "isPaid",
            formType: "checkbox" as const,
            required: true,
        },
    ];

    return (
        <Container fluid className="px-4 py-3">
            {error && <Alert variant="warning">Error: {error.message}</Alert>}
            <div className="d-flex justify-content-center align-items-center gap-3 mt-3">
                <PdfPreview file={file}/>
                <SubmissionForm<InvoiceFormData>
                    name="Invoice"
                    submit={(data: InvoiceFormData) =>
                        submitInvoice(file, mapInvoicetoCreateInvoice(data))
                    }
                    formGroups={formGroups}
                    initialData={initialInvoice}
                    additionalItems={clients}
                />
            </div>
        </Container>
    );
}

export default InvoiceForm;
