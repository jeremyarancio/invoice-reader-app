import { useFetchInvoices } from "@/hooks/api/invoice";
import { useFetchClients } from "@/hooks/api/client";
import { useCurrencyStore, type Currency } from "@/stores/currencyStore";

export function useDashboard(): {
    revenueChartData: {
        clientName: string;
        grossAmount: number;
        issuedDate: Date;
        paidDate?: Date;
    }[];
    selectedCurrency: Currency;
    totalRevenue: number;
    nPendingInvoice: number;
    totalPendingRevenue: number;
    availableYears: string[];
    isLoading: boolean;
    error: Error | null;
    hasData: boolean;
} {
    const { selectedCurrency } = useCurrencyStore();
    const {
        invoices,
        isLoading: invoicesLoading,
        error: invoicesError,
    } = useFetchInvoices(1, 1000);
    const {
        clients,
        isLoading: clientsLoading,
        error: clientsError,
    } = useFetchClients(1, 100);

    const hasData = (invoices?.length ?? 0) > 0;
    const error = invoicesError || clientsError;
    const isLoading = invoicesLoading || clientsLoading;

    const availableYears = Array.from(
        new Set(invoices.map((item) => new Date(item.issuedDate).getFullYear()))
    )
        .sort((a, b) => b - a)
        .map((year) => year.toString());

    const revenueChartData = invoices.map((invoice) => {
        return {
            issuedDate: invoice.issuedDate,
            paidDate: invoice.paidDate,
            grossAmount: invoice.grossAmount,
            clientName:
                clients.find((c) => c.id === invoice.clientId)?.clientName ||
                "Unknown",
        };
    });

    const totalRevenue = invoices.reduce(
        (sum, invoice) => sum + invoice.grossAmount,
        0
    );

    const nPendingInvoice = invoices.filter(
        (invoice) => !invoice.paidDate
    ).length;

    const totalPendingRevenue = invoices
        .filter((invoice) => !invoice.paidDate)
        .reduce((sum, invoice) => sum + invoice.grossAmount, 0);

    return {
        revenueChartData,
        selectedCurrency,
        totalRevenue,
        nPendingInvoice,
        totalPendingRevenue,
        availableYears,
        error,
        isLoading,
        hasData,
    };
}
