import { Area, AreaChart, CartesianGrid, XAxis, YAxis } from "recharts";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import {
    type ChartConfig,
    ChartContainer,
    ChartTooltip,
    ChartTooltipContent,
} from "@/components/ui/chart";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { useState } from "react";

const chartData = [
    { date: "2024-01-27", clientName: "Epam", invoiced: 4500, pending: 0 },
    { date: "2024-07-28", clientName: "Epam", invoiced: 2800, pending: 0 },
    { date: "2024-09-29", clientName: "SAP", invoiced: 0, pending: 2200 },
    { date: "2024-10-30", clientName: "Epam", invoiced: 8500, pending: 0 },
    { date: "2025-01-27", clientName: "Epam", invoiced: 100, pending: 0 },
    { date: "2025-07-28", clientName: "Epam", invoiced: 4500, pending: 0 },
    { date: "2025-09-29", clientName: "SAP", invoiced: 2500, pending: 0 },
    { date: "2025-10-30", clientName: "Epam", invoiced: 3000, pending: 8500 },
];

const chartConfig = {
    invoiced: {
        label: "Invoiced",
        color: "var(--chart-1)",
    },
    pending: {
        label: "Pending",
        color: "var(--chart-2)",
    },
} satisfies ChartConfig;

function RevenueChart() {
    const now = new Date();
    const [selectedYear, setSelectedYear] = useState(
        now.getFullYear().toString()
    );

    // Filter data for selected year
    const year = parseInt(selectedYear);
    const yearStart = new Date(year, 0, 1);
    const yearEnd = new Date(year, 11, 31, 23, 59, 59);

    const yearData = chartData.filter((item) => {
        const date = new Date(item.date);
        return date >= yearStart && date <= yearEnd;
    });

    // Add January 1st starting point if not already present
    const dataWithStart = [
        { date: `${year}-01-01`, clientName: "Start", invoiced: 0, pending: 0 },
        ...yearData.filter((item) => item.date !== `${year}-01-01`),
    ];

    // Accumulate invoiced and pending values from start of year
    const accumulateData = (data: typeof chartData) => {
        let cumulativeInvoiced = 0;
        let cumulativePending = 0;

        return data.map((item) => {
            cumulativeInvoiced += item.invoiced;
            cumulativePending += item.pending;

            return {
                ...item,
                invoiced: cumulativeInvoiced,
                pending: cumulativePending,
            };
        });
    };

    const filteredData = accumulateData(dataWithStart);

    return (
        <Card className="pt-0">
            <CardHeader className="flex items-center gap-2 space-y-0 py-5 sm:flex-row">
                <div className="grid flex-1 gap-1">
                    <CardTitle>Revenue</CardTitle>
                    <CardDescription>Monthly revenue</CardDescription>
                </div>
                <Select value={selectedYear} onValueChange={setSelectedYear}>
                    <SelectTrigger
                        className="hidden w-[160px] rounded-lg sm:ml-auto sm:flex"
                        aria-label="Select a year"
                    >
                        <SelectValue placeholder="Select year" />
                    </SelectTrigger>
                    <SelectContent className="rounded-xl">
                        <SelectItem value="2024" className="rounded-lg">
                            2024
                        </SelectItem>
                        <SelectItem value="2025" className="rounded-lg">
                            2025
                        </SelectItem>
                        <SelectItem value="2026" className="rounded-lg">
                            2026
                        </SelectItem>
                    </SelectContent>
                </Select>
            </CardHeader>
            <CardContent className="px-2 pt-4 sm:px-6 sm:pt-6">
                <ChartContainer
                    config={chartConfig}
                    className="aspect-auto h-[250px] w-full"
                >
                    <AreaChart data={filteredData}>
                        <defs>
                            <linearGradient
                                id="filInvoiced"
                                x1="0"
                                y1="0"
                                x2="0"
                                y2="1"
                            >
                                <stop
                                    offset="5%"
                                    stopColor="var(--color-invoiced)"
                                    stopOpacity={0.8}
                                />
                                <stop
                                    offset="95%"
                                    stopColor="var(--color-invoiced)"
                                    stopOpacity={0.1}
                                />
                            </linearGradient>
                            <linearGradient
                                id="fillPending"
                                x1="0"
                                y1="0"
                                x2="0"
                                y2="1"
                            >
                                <stop
                                    offset="5%"
                                    stopColor="var(--color-pending)"
                                    stopOpacity={0.8}
                                />
                                <stop
                                    offset="95%"
                                    stopColor="var(--color-pending)"
                                    stopOpacity={0.1}
                                />
                            </linearGradient>
                        </defs>
                        <CartesianGrid vertical={false} />
                        <XAxis
                            dataKey="date"
                            tickLine={false}
                            axisLine={false}
                            tickMargin={8}
                            minTickGap={32}
                            tickFormatter={(value) => {
                                const date = new Date(value);
                                return date.toLocaleDateString("en-EU", {
                                    month: "short",
                                    day: "numeric",
                                });
                            }}
                        />
                        <YAxis
                            tickLine={false}
                            axisLine={false}
                            tickMargin={10}
                        />
                        <ChartTooltip
                            cursor={true}
                            content={
                                <ChartTooltipContent
                                    indicator="line"
                                    labelFormatter={(value) => {
                                        return new Date(value).toLocaleDateString("en-EU", {
                                            month: "short",
                                            day: "numeric",
                                        });
                                    }}
                                    formatter={(value, name, item) => (
                                        <div className="flex flex-col gap-1">
                                            {item.payload.clientName && (
                                                <span className="text-xs text-muted-foreground">
                                                    {item.payload.clientName}
                                                </span>
                                            )}
                                            <span>
                                                {name}: ${Number(value).toLocaleString()}
                                            </span>
                                        </div>
                                    )}
                                />
                            }
                        />
                        <Area
                            dataKey="invoiced"
                            type="monotoneY"
                            fill="url(#filInvoiced)"
                            stroke="var(--color-invoiced)"
                            stackId="a"
                        />
                        <Area
                            dataKey="pending"
                            type="monotoneY"
                            fill="url(#fillPending)"
                            stroke="var(--color-pending)"
                            stackId="a"
                        />
                    </AreaChart>
                </ChartContainer>
            </CardContent>
        </Card>
    );
}

export default RevenueChart;
