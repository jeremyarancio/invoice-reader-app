import { useNavigate } from "react-router-dom";
import { mapInvoiceToPutInvoice } from "./mappers";
import { deleteInvoices, updateInvoice } from "../../services/api";
import { useMutation } from "@tanstack/react-query";
import { queryClient } from "../../services/api";
import { Invoice } from "./types";

export const onAddInvoice = () => {
    const navigate = useNavigate();
    navigate("/upload");
};

export const onUpdateInvoice = (invoice: Invoice) => {
    const updateMutation = useMutation({
        mutationFn: updateInvoice,
        onSuccess: () => {
            window.alert("Successfully updated.");
            queryClient.invalidateQueries({ queryKey: ["invoices"] });
        },
        onError: (err) => {
            const errorMessage =
                err instanceof Error
                    ? err.message
                    : "An unexpected error occurred";
            window.alert("Error: " + errorMessage);
        },
    });
    updateMutation.mutate(mapInvoiceToPutInvoice(invoice));
};

export const onDeleteInvoices = (invoices: Invoice[]) => {
    const deleteMutation = useMutation({
        mutationFn: deleteInvoices,
        onSuccess: () => {
            window.alert("Successfully deleted");
            queryClient.invalidateQueries({ queryKey: ["invoices"] });
        },
        onError: (error: Error) => {
            window.alert("Failed to delete: " + error.message);
        },
    });

    const invoiceIds = invoices.map((invoice) => invoice.id);
    deleteMutation.mutate(invoiceIds);
};
