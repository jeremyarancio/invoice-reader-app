import { useNavigate } from "react-router-dom";
import { mapInvoiceToPutInvoice } from "./mappers";
import { deleteInvoices, updateInvoice, submitInvoice } from "@/services/api";
import { useMutation, useQuery } from "@tanstack/react-query";
import { queryClient, fetchCurrencies } from "@/services/api";
import { CreateInvoicePayload, Invoice } from "./types";
import { AxiosError } from "axios";

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
            queryClient.invalidateQueries({ queryKey: ["clients"] });
        },
        onError: (error: AxiosError) => {
            error.status === 409
                ? window.alert(
                      "Error: Invoice already exists. Submission aborted."
                  )
                : window.alert(
                      "Error: " + (error.response?.data as any)?.message
                  );
        },
    });
    return (file: File, data: CreateInvoicePayload) =>
        addInvoiceMutation.mutate({ file, data });
};

export const useUpdateInvoice = () => {
    const updateMutation = useMutation({
        mutationFn: updateInvoice,
        onSuccess: () => {
            window.alert("Successfully updated.");
            queryClient.invalidateQueries({ queryKey: ["invoices"] });
        },
        onError: (error: AxiosError) => {
            window.alert("Error: " + error.message);
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
        deleteMutation.mutate(invoiceIds);
    };
};

export const useFetchCurrencies = () => {
    return () =>
        useQuery({
            queryKey: ["currencies"],
            queryFn: () => fetchCurrencies(),
        });
};
