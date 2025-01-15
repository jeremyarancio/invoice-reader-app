import { useNavigate } from "react-router-dom";
import { mapInvoiceToPutInvoice } from "./mappers";
import {
    deleteInvoices,
    updateInvoice,
    fetchInvoices,
    submitInvoice,
} from "../../services/api";
import { useMutation, useQuery } from "@tanstack/react-query";
import { queryClient } from "../../services/api";
import { CreateInvoicePayload, Invoice } from "./types";

export const useAddInvoice = () => {
    const navigate = useNavigate();
    return () => navigate("/upload");
};

export const useSubmitInvoice = () => {
    const addInvoiceMutation = useMutation({
        mutationFn: ({
            file,
            data,
        }: {
            file: File;
            data: CreateInvoicePayload;
        }) => submitInvoice(file, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["invoices"] });
        },
        onError: (error: Error) => {
            console.error(error);
        },
    });
    return (file: File, data: CreateInvoicePayload) =>
        addInvoiceMutation.mutate({ file, data });
};

export const useFetchInvoices = () => {
    return (pageNumber: number, perPage: number) =>
        useQuery({
            queryKey: ["invoices", pageNumber, perPage],
            queryFn: () => fetchInvoices(pageNumber, perPage),
            enabled: !!sessionStorage.getItem("accessToken"),
        });
};

export const useUpdateInvoice = () => {
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
    return (invoice: Invoice) =>
        updateMutation.mutate(mapInvoiceToPutInvoice(invoice));
};

export const useDeleteInvoices = () => {
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
    return (invoices: Invoice[]) => {
        const invoiceIds = invoices.map((invoice) => invoice.id);
        return () => deleteMutation.mutate(invoiceIds);
    };
};
