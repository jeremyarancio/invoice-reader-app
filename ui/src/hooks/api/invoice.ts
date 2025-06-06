import {
    mapGetCurrencyToCurrency,
    mapGetInvoiceToInvoice,
} from "@/lib/mappers/invoice";
import { fetchCurrencies, fetchInvoices } from "@/services/api/invoice";
import { useQuery } from "@tanstack/react-query";

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
