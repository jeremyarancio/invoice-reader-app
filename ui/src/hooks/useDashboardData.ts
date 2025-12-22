import type { MonthlyChartData } from "@/components/dashboard/RevenueChart";
import type { MonthlyRevenues } from "@/schemas/analytics";
import { fetchMonthlyRevenues } from "@/services/api/analytics";
import { useCurrencyStore, type Currency } from "@/stores/currencyStore";
import { useQuery } from "@tanstack/react-query";

export const useFetchMonthlyRevenues = (year: string, currency: Currency) => {
    const { data, isLoading, error } = useQuery({
        queryKey: ["monthlyRevenues", year, currency],
        queryFn: () => fetchMonthlyRevenues(year, currency),
    });

    return { data, isLoading, error };
};

const convertDataToChartFormat = (
    data: MonthlyRevenues[]
): MonthlyChartData[] => {
    let cumulativeInvoiced = 0;
    let cumulativePending = 0;

    const monthlyChartData = data.map((monthData) => {
        cumulativeInvoiced += monthData.totalInvoiced;
        cumulativePending += monthData.totalPending;

        return {
            month: monthData.month,
            accumulatedInvoiced: cumulativeInvoiced,
            accumulatedPending: cumulativePending,
            sumInvoiced: monthData.totalInvoiced,
            sumPending: monthData.totalPending,
            clientRevenue: monthData.clients.map((client) => ({
                clientName: client.clientName,
                sumInvoiced: client.totalInvoiced,
                sumPending: client.totalPending,
            })),
        };
    });

    return monthlyChartData;
};

export function useDashboard(selectedYear: string): {
    totalRevenue: number;
    totalPending: number;
    monthlyChartData: MonthlyChartData[];
    isLoading: boolean;
    error: Error | null;
    hasData: boolean;
} {
    const { selectedCurrency } = useCurrencyStore();
    const {
        data: monthlyRevenues,
        isLoading,
        error,
    } = useFetchMonthlyRevenues(selectedYear, selectedCurrency);

    const hasData = !!monthlyRevenues && monthlyRevenues.revenues.length > 0;

    const totalRevenue =
        monthlyRevenues?.revenues.reduce(
            (sum, revenue) => sum + revenue.totalInvoiced,
            0
        ) ?? 0;

    const totalPending =
        monthlyRevenues?.revenues.reduce(
            (sum, revenue) => sum + revenue.totalPending,
            0
        ) ?? 0;

    const monthlyChartData = monthlyRevenues?.revenues
        ? convertDataToChartFormat(monthlyRevenues.revenues)
        : [];

    return {
        totalRevenue,
        totalPending,
        monthlyChartData,
        error,
        isLoading,
        hasData,
    };
}
