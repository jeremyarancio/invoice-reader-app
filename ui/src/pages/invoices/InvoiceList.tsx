import { Alert } from "react-bootstrap";
import { Invoice } from "./types";
import TableRender from "../../common/components/TableRender";
import { mapGetInvoiceToInvoice } from "./mappers";
import {
    useAddInvoice,
    useDeleteInvoices,
    useFetchInvoices,
    useUpdateInvoice,
} from "./hooks";

const InvoiceList = () => {
    const pageNumber = 1;
    const perPage = 10;
    const addInvoice = useAddInvoice();
    const updateInvoice = useUpdateInvoice();
    const fetchInvoices = useFetchInvoices();
    const deleteInvoices = useDeleteInvoices();

    const { data, isLoading, error } = fetchInvoices(pageNumber, perPage);

    const invoices =
        data?.data.map((invoice) => mapGetInvoiceToInvoice(invoice)) || [];

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
                disabledFields={disabledFields}
                onAddItem={addInvoice}
                onUpdateItem={updateInvoice}
                onDeleteItems={deleteInvoices}
            />
        </>
    );
};

export default InvoiceList;
