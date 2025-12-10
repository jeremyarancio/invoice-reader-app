import { useFetchUser } from "@/hooks/api/users";
import { CURRENCIES } from "@/schemas/invoice";
import type { Currency } from "@/stores/currencyStore";

interface DashboardHeaderProps {
    currency: Currency;
}

export function DashboardHeader({ currency }: DashboardHeaderProps) {
    const currencyName = CURRENCIES[currency]?.name || currency;
    const { user } = useFetchUser();

    return (
        <div className="flex sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
            <div className="space-y-2">
                <h1 className="text-3xl font-bold tracking-tight">
                    Welcome Jeremy!
                </h1>
                <p>{user?.email}</p>
            </div>
            <div className="flex items-center gap-2">
                <span className="text-sm text-muted-foreground">
                    Showing values in:
                </span>
                <span className="items-center rounded-md bg-primary/10 px-2.5 py-0.5 text-sm font-medium text-primary">
                    {currencyName} ({CURRENCIES[currency]?.symbol})
                </span>
            </div>
        </div>
    );
}
