import {
    mapGetCurrencyToCurrency,
    mapGetInvoiceToInvoice,
} from "@/lib/mappers/invoice";
import type { CreateInvoicePayload } from "@/schemas/invoice";
import {
    addInvoice,
    fetchCurrencies,
    fetchInvoices,
} from "@/services/api/invoice";
import { queryClient } from "@/services/api/main";
import { useMutation, useQuery } from "@tanstack/react-query";
import type { AxiosError } from "axios";

export const useFetchCurrencies = () => {
    return () => {
        const { data, isLoading, error } = useQuery({
            queryKey: ["currencies"],
            queryFn: () => fetchCurrencies(),
        });
        const currencies = data?.map(mapGetCurrencyToCurrency) || [];
        return { currencies, isLoading, error };
    };
};

export const useFetchInvoices = () => {
    return (pageNumber: number = 1, perPage: number = 10) => {
        const { data, isLoading, error } = useQuery({
            queryKey: ["invoices", pageNumber, perPage],
            queryFn: () => fetchInvoices(pageNumber, perPage),
        });
        const invoices = data?.data.map(mapGetInvoiceToInvoice) || [];

        return { invoices, isLoading, error };
    };
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
        addInvoiceMutation.mutate({ file, data });
};
