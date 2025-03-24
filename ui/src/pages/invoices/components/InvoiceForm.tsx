import { Invoice } from "../types";
import { useFetchClients } from "@/pages/clients/hooks";
import { useFetchCurrencies, useSubmitInvoice } from "../hooks";
import SubmissionForm from "@/common/components/SubmissionForm";
import { mapGetClientToClient } from "@/pages/clients/mapper";
import {
    mapGetCurrencyToCurrency,
    mapInvoicetoCreateInvoice,
} from "../mappers";
import { Col, Container, Row } from "react-bootstrap";
import PdfPreview from "@/common/components/PdfPreview";
import { useState } from "react";
import AlertError from "@/common/components/AlertError";

type InvoiceFormData = Omit<Invoice, "id">;

interface FormProperties {
    file: File;
}

const initialInvoice: InvoiceFormData = {
    amountExcludingTax: 0,
    vat: 0,
    invoicedDate: new Date(),
    invoiceNumber: "",
    clientId: "",
    isPaid: false,
    currencyId: "000000",
};

function InvoiceForm({ file }: FormProperties) {
    const [error, setError] = useState<Error | null>(null);
    const fetchClients = useFetchClients();
    const submitInvoice = useSubmitInvoice();
    const fetchCurrencies = useFetchCurrencies();

    const { data: pagedClients, error: fetchClientsError } = fetchClients();
    const clients = pagedClients?.data.map(mapGetClientToClient) || [];

    const { data: getCurrencies, error: fetchCurrenciesError } =
        fetchCurrencies();
    const currencies = getCurrencies?.map(mapGetCurrencyToCurrency) || [];

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
            key: "currencyId",
            formType: "select" as const,
            required: true,
            fetchedItems: currencies,
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
            fetchedItems: clients,
        },
        {
            header: "Paid?",
            key: "isPaid",
            formType: "checkbox" as const,
        },
    ];

    fetchClientsError && setError(fetchClientsError);
    fetchCurrenciesError && setError(fetchCurrenciesError);

    return (
        <Container fluid>
            <>
                {error && (
                    <AlertError error={error} onClose={() => setError(null)} />
                )}
                <Row>
                    <Col>
                        <PdfPreview file={file} />
                    </Col>
                    <Col>
                        <SubmissionForm<InvoiceFormData>
                            name="Invoice"
                            submit={(data: InvoiceFormData) =>
                                submitInvoice(
                                    file,
                                    mapInvoicetoCreateInvoice(data)
                                )
                            }
                            formGroups={formGroups}
                            initialData={initialInvoice}
                        />
                    </Col>
                </Row>
            </>
        </Container>
    );
}

export default InvoiceForm;
