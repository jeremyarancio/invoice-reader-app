import { useState, useEffect } from "react";
import { Alert } from "react-bootstrap";
import {
    fetchInvoices,
    updateInvoice,
    deleteInvoices,
} from "../../services/api";
import { useMutation } from "@tanstack/react-query";
import { InvoiceRender, GetInvoicesResponse } from "../../types";
import { useNavigate } from "react-router-dom";
import TableRender from "../../common/components/TableRender";

const InvoiceList = () => {
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const navigate = useNavigate();

    const InvoiceListMutation = useMutation({
        mutationFn: fetchInvoices,
        onSuccess: (response: GetInvoicesResponse) => {
            setError(null);
            const ExtractedInvoiceRender: InvoiceRender[] = response.data.map(
                (item) => ({
                    data: {
                        invoice_id: item.invoice_id,
                        invoice_number: item.data.invoice_number,
                        client_id: item.data.client_id,
                        currency: item.data.currency,
                        invoiced_date: item.data.invoiced_date,
                        amount_excluding_tax: item.data.amount_excluding_tax,
                        vat: item.data.vat,
                    },
                    clientName: item.data.client_id,
                    paid: true,
                })
            );

            setInvoiceRenderList(ExtractedInvoiceRender);
            setTotalInvoices(response.total);
            setIsLoading(false);
        },
        onError: (error: Error) => {
            setError(error.message || "Failed to load invoices.");
            console.error(error);
            setIsLoading(false);
        },
    });

    useEffect(() => {
        const fetchInvoices = () => {
            setIsLoading(true);
            setError(null);
            InvoiceListMutation.mutate({ pageNumber, perPage });
        };

        fetchInvoices();
    }, [pageNumber, perPage]);

    
    const updateMutation = useMutation({
        mutationFn: updateInvoice,
        onSuccess: () => {
            window.alert("Successfully updated.");
            onClose();
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

    const AddInvoice = () => {
        navigate("/upload");
    };

    const updateInvoice = () => {}
    const deleteInvoices = () => {}

    if (isLoading) return <div>Loading invoices...</div>;
    if (!sessionStorage.getItem("accessToken"))
        return (
            <Alert variant="danger">Log in to visualize your invoices...</Alert>
        );

    return (
        <>
            <TableRender 
                name="Invoice" 
                items={invoices}
                columns={}
                disabled={}
                onAddItem={}
                onUpdateItem={}
                onDeleteItems={}
            />
        </>
    );
};

export default InvoiceList;
