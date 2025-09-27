import {
    mapGetInvoiceToInvoice,
    mapInvoiceToUpdateInvoice,
} from "@/lib/mappers/invoice";
import type {
    CreateInvoicePayload,
    Invoice,
    UpdateInvoice,
} from "@/schemas/invoice";
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
    const addInvoiceMutation = useMutation({
        mutationFn: ({
            file,
            data,
        }: {
            file: File;
            data: CreateInvoicePayload;
        }) => addInvoice(file, data),
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
        addInvoiceMutation.mutateAsync({ file, data });
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
    const updateInvoiceMutation = useMutation({
        mutationFn: ({ invoice_id, data }: { invoice_id: string; data: UpdateInvoice }) => {
            return updateInvoice(invoice_id, data);
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["invoices"] });
            queryClient.invalidateQueries({ queryKey: ["invoice"] });
            window.alert("Invoice updated successfully");
        },
        onError: (error: AxiosError) => {
            window.alert("Error: " + (error.response?.data as any)?.message);
        },
    });
    return (invoice: Invoice) =>
        updateInvoiceMutation.mutateAsync({
            invoice_id: invoice.id,
            data: mapInvoiceToUpdateInvoice(invoice),
        });
};

export const useDeleteInvoice = () => {
    const deleteInvoicesMutation = useMutation({
        mutationFn: deleteInvoice,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["invoices"] });
            window.alert("Invoices deleted successfully");
        },
        onError: (error: AxiosError) => {
            error.status === 422
                ? window.alert(
                      "No invoice with this ID exists. Please try again."
                  )
                : window.alert(
                      "Error: " + (error.response?.data as any)?.message
                  );
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
