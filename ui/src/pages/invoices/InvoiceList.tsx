import { Alert } from "react-bootstrap";
import { fetchInvoices } from "../../services/api";
import { useQuery } from "@tanstack/react-query";
import { Invoice } from "./types";
import TableRender from "../../common/components/TableRender";
import { mapInvoicePayloadToInvoice } from "./mappers";
import { onUpdateInvoice, onDeleteInvoices, onAddInvoice } from "./hooks";

const InvoiceList = () => {
    const pageNumber = 1;
    const perPage = 10;

    const { data, isLoading, error } = useQuery({
        queryKey: ["invoices", pageNumber, perPage],
        queryFn: () => fetchInvoices({ pageNumber, perPage }),
        enabled: !!sessionStorage.getItem("accessToken"),
    });

    const invoices =
        data?.data.map((invoice) => mapInvoicePayloadToInvoice(invoice)) || [];

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

    const editFields = [
        {
            header: "Invoice number",
            key: "invoiceNumber",
        },
        {
            header: "Amount excluding tax",
            key: "amountExcludingTax",
        },
        {
            header: "VAT",
            key: "vat",
        },
        {
            header: "Invoiced date",
            key: "invoicedDate",
        },
    ];

    if (isLoading) return <div>Loading invoices...</div>;
    if (!sessionStorage.getItem("accessToken"))
        return (
            <Alert variant="danger">Log in to visualize your invoices...</Alert>
        );

    // Fields that should be disabled in the Edition mode
    const disabledFields = ["invoiceNumber", "invoicedDate"];

    return (
        <>
            {error && <Alert variant="warning">Error: {error.message}</Alert>}
            <TableRender<Invoice>
                name="Invoice"
                columns={tableColumns}
                items={invoices}
                editFields={editFields}
                disabled={disabledFields}
                onAddItem={onAddInvoice}
                onUpdateItem={onUpdateInvoice}
                onDeleteItems={onDeleteInvoices}
            />
        </>
    );
};

export default InvoiceList;
