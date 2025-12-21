import type { Currency } from "@/stores/currencyStore";

type ClientMonthBreakdowm = {
    clientName: string;
    totalInvoiced: number;
    totalPending: number;
};

export type MonthlyRevenues = {
    month: number;
    totalInvoiced: number;
    totalPending: number;
    clients: ClientMonthBreakdowm[];
};
export type GetMonthlyRevenues = {
    selectedCurrency: Currency;
    year: number;
    revenues: MonthlyRevenues[];
};
