import { Invoice } from "../types";
import TableRender from "@/common/components/TableRender";
import { mapGetInvoiceToInvoice } from "../mappers";
import { useAddInvoice, useDeleteInvoices, useUpdateInvoice } from "../hooks";
import { useQuery } from "@tanstack/react-query";
import { fetchInvoices, fetchInvoiceUrl } from "@/services/api";
import { Alert } from "react-bootstrap";

const InvoiceList = () => {
    const pageNumber = 1;
    const perPage = 10;
    const addInvoice = useAddInvoice();
    const updateInvoice = useUpdateInvoice();
    const deleteInvoices = useDeleteInvoices();

    // Fetch invoices
    const {
        data: invoiceData,
        isLoading,
        error,
    } = useQuery({
        queryKey: ["invoices", pageNumber, perPage],
        queryFn: () => fetchInvoices(pageNumber, perPage),
        enabled: !!sessionStorage.getItem("accessToken"),
    });

    const invoices =
        invoiceData?.data.map((invoice) => mapGetInvoiceToInvoice(invoice)) ||
        [];

    // Fetch invoice URLs
    const { data: invoiceURLs } = useQuery({
        queryKey: ["invoiceUrls", invoices.map((invoice) => invoice.id)],
        queryFn: async () => {
            const urls = await Promise.all(
                invoices.map((invoice: Invoice) => fetchInvoiceUrl(invoice.id))
            );
            return urls;
        },
        enabled: !!sessionStorage.getItem("accessToken") && invoices.length > 0,
    });

    const invoicePreviews = invoices.map((invoice, index) => ({
        id: invoice.id,
        file: invoiceURLs?.[index] ?? null,
    }));

    if (isLoading) return <div>Loading invoices...</div>;
    if (!sessionStorage.getItem("accessToken"))
        return (
            <Alert variant="danger">Log in to visualize your invoices...</Alert>
        );

    return (
        <>
            {error && <Alert variant="warning">Error: {error.message}</Alert>}
            <TableRender<Invoice>
                name="Invoices"
                items={invoices}
                columns={[
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
                        render: (item: Invoice) =>
                            `${item.currency}${item.amountExcludingTax.toFixed(
                                2
                            )}`,
                    },
                    {
                        header: "Paid?",
                        key: "isPaid",
                        render: (item: Invoice) => (item.isPaid ? "Yes" : "No"),
                    },
                ]}
                editFields={[
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
                    {
                        header: "Paid?",
                        key: "isPaid",
                    },
                ]}
                disabledFields={["invoiceNumber"]} // Fields that should be disabled in the Edition mode
                onAddItem={addInvoice}
                onUpdateItem={updateInvoice}
                onDeleteItems={deleteInvoices}
                filePreviews={invoicePreviews}
            />
        </>
    );
};

export default InvoiceList;
