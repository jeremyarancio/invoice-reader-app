import {
    mapGetCurrencyToCurrency,
    mapGetInvoiceToInvoice,
} from "@/lib/mappers/invoice";
import { fetchCurrencies, fetchInvoices } from "@/services/api/invoice";
import { useQuery } from "@tanstack/react-query";

export const useFetchInvoices = () => {
    const { data, isLoading, error } = useQuery({
        queryKey: ["invoices"],
        queryFn: () => fetchInvoices(),
    });

    const invoices = data?.data.map(mapGetInvoiceToInvoice);
    return { invoices, isLoading, error };
};

export const useFetchCurrencies = () => {
    const { data, isLoading, error } = useQuery({
        queryKey: ["currencies"],
        queryFn: () => fetchCurrencies(),
    });

    const currencies = data?.map(mapGetCurrencyToCurrency) || [];
    return { currencies, isLoading, error };
};
