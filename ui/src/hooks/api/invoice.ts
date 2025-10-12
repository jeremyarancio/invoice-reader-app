import {
    mapGetInvoiceToInvoice,
    mapInvoiceDataToCreateInvoice,
    mapInvoiceDataToPayload,
} from "@/lib/mappers/invoice";
import type { InvoiceData, UpdateInvoice } from "@/schemas/invoice";
import {
    addInvoice,
    deleteInvoice,
    fetchInvoice,
    fetchInvoices,
    fetchInvoiceUrl,
    parseInvoice,
    updateInvoice,
} from "@/services/api/invoice";
import { queryClient } from "@/services/api/main";
import { useMutation, useQuery } from "@tanstack/react-query";
import type { AxiosError } from "axios";
import { useAlert } from "@/contexts/AlertContext";

export const useFetchInvoices = (
    pageNumber: number = 1,
    perPage: number = 10
) => {
    const { data, isLoading, error } = useQuery({
        queryKey: ["invoices", pageNumber, perPage],
        queryFn: () => fetchInvoices(pageNumber, perPage),
    });
    const invoices = data?.invoices.map(mapGetInvoiceToInvoice) || [];

    return { invoices, isLoading, error };
};

export const useFetchInvoiceUrl = (invoiceId: string | undefined) => {
    const { data, isLoading, error } = useQuery({
        queryKey: ["invoices", invoiceId],
        queryFn: () => fetchInvoiceUrl(invoiceId as string),
        enabled: !!invoiceId,
    });
    const url = data || null;
    return { url, isLoading, error };
};

export const useAddInvoice = () => {
    const { showAlert } = useAlert();

    const addInvoiceMutation = useMutation({
        mutationFn: ({
            file,
            invoiceData,
            clientId,
        }: {
            file: File;
            invoiceData: InvoiceData;
            clientId: string;
        }) => {
            const payload = mapInvoiceDataToCreateInvoice(
                invoiceData,
                clientId
            );
            return addInvoice(file, payload);
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["invoices"] });
            queryClient.invalidateQueries({ queryKey: ["clients"] });
            showAlert("success", "Success!", "Invoice created successfully");
        },
        onError: (error: AxiosError) => {
            const message =
                error.status === 409
                    ? "Invoice already exists. Submission aborted."
                    : (error.response?.data as any)?.message;

            showAlert("error", "Error", message);
        },
    });
    return (file: File, invoiceData: InvoiceData, clientId: string) =>
        addInvoiceMutation.mutateAsync({ file, invoiceData, clientId });
};

export const useFetchInvoice = (invoiceId: string | undefined) => {
    const { data, isLoading, error } = useQuery({
        queryKey: ["invoice", invoiceId],
        queryFn: () => fetchInvoice(invoiceId as string),
        enabled: !!invoiceId,
    });
    const invoice = data ? mapGetInvoiceToInvoice(data) : null;
    return { invoice, isLoading, error };
};

export const useUpdateInvoice = () => {
    const { showAlert } = useAlert();

    const updateInvoiceMutation = useMutation({
        mutationFn: ({
            invoice_id,
            invoiceData,
            clientId,
        }: {
            invoice_id: string;
            invoiceData: InvoiceData;
            clientId: string;
        }) => {
            const updateData: UpdateInvoice = {
                client_id: clientId,
                data: mapInvoiceDataToPayload(invoiceData),
            };
            return updateInvoice(invoice_id, updateData);
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["invoices"] });
            queryClient.invalidateQueries({ queryKey: ["invoice"] });
            showAlert("success", "Updated!", "Invoice updated successfully");
        },
        onError: (error: AxiosError) => {
            error.response?.status === 409
                ? showAlert(
                      "error",
                      "Error",
                      "Invoice with this number already exists. Update aborted."
                  )
                : showAlert(
                      "error",
                      "Error",
                      "Something went wrong. Please try again later."
                  );
        },
    });
    return (invoiceId: string, invoiceData: InvoiceData, clientId: string) =>
        updateInvoiceMutation.mutateAsync({
            invoice_id: invoiceId,
            invoiceData,
            clientId,
        });
};

export const useDeleteInvoice = () => {
    const { showAlert } = useAlert();

    const deleteInvoicesMutation = useMutation({
        mutationFn: deleteInvoice,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["invoices"] });
            showAlert("success", "Deleted!", "Invoice deleted successfully");
        },
        onError: (error: AxiosError) => {
            const message =
                error.status === 422
                    ? "No invoice with this ID exists. Please try again."
                    : "Error: Something went wrong. Please try again later.";

            showAlert("error", "Error", message);
        },
    });
    return (invoiceId: string) => deleteInvoicesMutation.mutate(invoiceId);
};

export const useParseInvoice = (file: File) => {
    const { data, isLoading, error } = useQuery({
        queryKey: ["parsing", file?.name],
        queryFn: () => parseInvoice(file),
        enabled: !!file,
    });
    return { data, isLoading, error };
};
