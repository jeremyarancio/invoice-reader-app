import { Alert } from "react-bootstrap";
import {
    fetchInvoices,
    updateInvoice,
    deleteInvoices,
} from "../../services/api";
import { useMutation, useQuery } from "@tanstack/react-query";
import { Invoice } from "./types";
import { useNavigate } from "react-router-dom";
import TableRender from "../../common/components/TableRender";
import {
    mapInvoicePayloadToInvoice,
    mapInvoiceToPutInvoice,
} from "../../utils/mappers";

const InvoiceList = () => {
    const navigate = useNavigate();
    const pageNumber = 1;
    const perPage = 10;

    const { data, isLoading, error } = useQuery({
        queryKey: ["invoices", pageNumber, perPage],
        queryFn: () => fetchInvoices({ pageNumber, perPage }),
        enabled: !!sessionStorage.getItem("accessToken"),
    });

    const updateMutation = useMutation({
        mutationFn: updateInvoice,
        onSuccess: () => {
            window.alert("Successfully updated.");
        },
        onError: (err) => {
            const errorMessage =
                err instanceof Error
                    ? err.message
                    : "An unexpected error occurred";
            window.alert("Error: " + errorMessage);
        },
    });

    const deleteMutation = useMutation({
        mutationFn: deleteInvoices,
        onSuccess: () => {
            window.alert("Successfully deleted");
        },
        onError: (error: Error) => {
            window.alert("Failed to delete: " + error.message);
        },
    });

    const invoices =
        data?.data.map((invoice) => mapInvoicePayloadToInvoice(invoice)) || [];

    const onAddInvoice = () => {
        navigate("/upload");
    };

    const onUpdateInvoice = (invoice: Invoice) => {
        updateMutation.mutate(mapInvoiceToPutInvoice(invoice));
    };

    const onDeleteInvoices = (invoices: Invoice[]) => {
        deleteMutation.mutate(invoices.map((invoice) => invoice.id));
    };

    const tableColumns = [
        {
            header: "Invoice Number",
            key: "invoiceNumber",
        },
        {
            header: "Date",
            key: "invoicedDate",
            render: (item: Invoice) =>
                new Date(item.invoicedDate).toLocaleDateString(),
        },
        {
            header: "Amount",
            key: "amount",
            render: (item: Invoice) => `$${item.amountExcludingTax.toFixed(2)}`,
        },
        {
            header: "Status",
            key: "paid_status", // Not implemented yet
        },
    ];

    if (isLoading) return <div>Loading invoices...</div>;
    if (!sessionStorage.getItem("accessToken"))
        return (
            <Alert variant="danger">Log in to visualize your invoices...</Alert>
        );

    // Fields that should be disabled in the Edition mode
    const disabledFields = ["invoice_number", "invoiced_date"];

    return (
        <>
            {error && <Alert variant="warning">Error: {error.message}</Alert>}
            <TableRender<Invoice>
                name="Invoice"
                columns={tableColumns}
                items={invoices}
                disabled={disabledFields}
                onAddItem={onAddInvoice}
                onUpdateItem={onUpdateInvoice}
                onDeleteItems={onDeleteInvoices}
            />
        </>
    );
};

export default InvoiceList;
