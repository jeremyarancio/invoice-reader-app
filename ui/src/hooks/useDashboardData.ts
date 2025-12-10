import { useMemo } from "react";
import { useFetchInvoices } from "@/hooks/api/invoice";
import { useFetchClients } from "@/hooks/api/client";
import { useCurrencyStore } from "@/stores/currencyStore";
import {
    calculateDashboardMetrics,
    type DashboardMetrics,
} from "@/lib/utils/dashboardCalculations";

interface UseDashboardDataReturn {
    metrics: DashboardMetrics | null;
    isLoading: boolean;
    error: Error | null;
    hasData: boolean;
}
export function useDashboardData(): UseDashboardDataReturn {
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

    const isLoading = invoicesLoading || clientsLoading;
    const error = (invoicesError || clientsError) as Error | null;

    const metrics = useMemo(() => {
        if (!invoices || !clients || invoices.length === 0) {
            return null;
        }

        return calculateDashboardMetrics(invoices, clients, selectedCurrency);
    }, [invoices, clients, selectedCurrency]);

    const hasData = (invoices?.length ?? 0) > 0 || (clients?.length ?? 0) > 0;

    return {
        metrics,
        isLoading,
        error,
        hasData,
    };
}
