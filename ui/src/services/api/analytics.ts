import type { GetMonthlyRevenues } from "@/schemas/analytics";
import { api } from "@/services/api/main";
import type { Currency } from "@/stores/currencyStore";

export const fetchMonthlyRevenues = async (
    year: string,
    currency: Currency
): Promise<GetMonthlyRevenues> => {
    const response = await api.get("analytics/revenues/monthly", {
        params: { year: year, currency: currency },
    });
    return response.data;
};
