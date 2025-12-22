import { useFetchUser } from "@/hooks/api/users";
import { CURRENCIES } from "@/schemas/invoice";
import type { Currency } from "@/stores/currencyStore";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";

interface DashboardHeaderProps {
    currency: Currency;
    selectedYear: string;
    availableYears: string[];
    setSelectedYear: (year: string) => void;
}

export function DashboardHeader({
    currency,
    selectedYear,
    availableYears,
    setSelectedYear,
}: DashboardHeaderProps) {
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
                    {CURRENCIES[currency]?.symbol}
                </span>
                <Select value={selectedYear} onValueChange={setSelectedYear}>
                    <SelectTrigger
                        className="hidden w-[160px] rounded-lg sm:ml-auto sm:flex"
                        aria-label="Select a year"
                    >
                        <SelectValue placeholder="Select year" />
                    </SelectTrigger>
                    <SelectContent className="rounded-xl">
                        {availableYears.map((year) => (
                            <SelectItem
                                key={year}
                                value={year.toString()}
                                className="rounded-lg"
                            >
                                {year}
                            </SelectItem>
                        ))}
                    </SelectContent>
                </Select>
            </div>
        </div>
    );
}
