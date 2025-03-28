import { Currency, Invoice } from "../types";
import TableRender from "@/common/components/TableRender";
import { mapGetCurrencyToCurrency, mapGetInvoiceToInvoice } from "../mappers";
import {
    useAddInvoice,
    useDeleteInvoices,
    useFetchCurrencies,
    useUpdateInvoice,
} from "../hooks";
import { useQuery } from "@tanstack/react-query";
import { fetchInvoices, fetchInvoiceUrl } from "@/services/api";
import { Alert } from "react-bootstrap";
import { useState } from "react";
import AlertError from "@/common/components/AlertError";

const InvoiceList = () => {
    const pageNumber = 1;
    const perPage = 10;
    const [error, setError] = useState<Error | null>(null);
    const addInvoice = useAddInvoice();
    const updateInvoice = useUpdateInvoice();
    const deleteInvoices = useDeleteInvoices();
    const fetchCurrencies = useFetchCurrencies();

    // Fetch invoices
    const {
        data: invoiceData,
        isLoading,
        error: fetchError,
    } = useQuery({
        queryKey: ["invoices", pageNumber, perPage],
        queryFn: () => fetchInvoices(pageNumber, perPage),
        enabled: !!localStorage.getItem("accessToken"),
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
        enabled: !!localStorage.getItem("accessToken") && invoices.length > 0,
    });

    const { data: getCurrencies } = fetchCurrencies();
    const currencies = getCurrencies?.map(mapGetCurrencyToCurrency);

    const invoicePreviews = invoices.map((invoice, index) => ({
        id: invoice.id,
        file: invoiceURLs?.[index] ?? null,
    }));

    const convertIdToCurrency = (
        currencyId: string,
        currencies: Currency[]
    ): string => {
        const currency = currencies.find((c) => c.id === currencyId);
        if (!currency) {
            throw new Error(`Currency with id ${currencyId} not found.`);
        }
        return currency.name;
    };

    if (isLoading) return <div>Loading invoices...</div>;
    fetchError && setError(fetchError);
    if (!localStorage.getItem("accessToken"))
        return (
            <Alert variant="danger">Log in to visualize your invoices...</Alert>
        );

    return (
        <>
            {error && (
                <AlertError error={error} onClose={() => setError(null)} />
            )}
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
                            `${
                                currencies
                                    ? convertIdToCurrency(
                                          item.currencyId,
                                          currencies
                                      )
                                    : ""
                            }${item.amountExcludingTax.toFixed(2)}`,
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
