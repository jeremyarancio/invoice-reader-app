import {
    ComposedChart,
    Area,
    CartesianGrid,
    XAxis,
    YAxis,
    Bar,
} from "recharts";
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

type MonthlyChartData = {
    //AreaChart
    month: number;
    accumulatedInvoiced: number;
    accumulatedPending: number;
    //BarChart
    sumInvoiced: number;
    sumPending: number;
    //ChartToolTip
    clientRevenue: {
        clientName: string;
        sumInvoiced: number;
        sumPending: number;
    }[];
};
const data = [
    {
        clientName: "Epam",
        gross_amount: 4500,
        issuedDate: new Date("2024-02-27"),
        paidDate: new Date("2024-03-05"),
    },
    {
        clientName: "SAP",
        gross_amount: 4500,
        issuedDate: new Date("2024-02-27"),
        paidDate: new Date("2024-03-05"),
    },
    {
        clientName: "Epam",
        gross_amount: 4500,
        issuedDate: new Date("2024-04-27"),
        paidDate: new Date("2024-04-28"),
    },
    {
        clientName: "SAP",
        gross_amount: 4500,
        issuedDate: new Date("2024-04-27"),
        paidDate: null,
    },
    {
        clientName: "Epam",
        gross_amount: 8500,
        issuedDate: new Date("2025-05-27"),
        paidDate: new Date("2025-06-05"),
    },
    {
        clientName: "Alma",
        gross_amount: 12500,
        issuedDate: new Date("2025-08-27"),
        paidDate: new Date("2025-09-05"),
    },
];

const chartConfig = {
    invoiced: {
        label: "Invoiced",
        color: "var(--chart-3)",
    },
    pending: {
        label: "Pending",
        color: "var(--chart-4)",
    },
} satisfies ChartConfig;

function RevenueChart() {
    const availableYears = Array.from(
        new Set(data.map((item) => new Date(item.issuedDate).getFullYear()))
    ).sort((a, b) => b - a);

    const [selectedYear, setSelectedYear] = useState(
        availableYears[0]?.toString() || new Date().getFullYear().toString()
    );

    const year = parseInt(selectedYear);

    const convertDataToChartFormat = (
        d: typeof data,
        year: number
    ): MonthlyChartData[] => {
        // Step 1: Generate all 12 months with initial values
        const monthlyData: MonthlyChartData[] = Array.from(
            { length: 12 },
            (_, month) => ({
                month: month,
                accumulatedInvoiced: 0,
                accumulatedPending: 0,
                sumInvoiced: 0,
                sumPending: 0,
                clientRevenue: [],
            })
        );

        // Step 2: Aggregate data by month and client
        d.forEach((item) => {
            const date = item.paidDate || item.issuedDate;
            if (date.getFullYear() !== year) return;

            const monthIndex = date.getMonth();
            const isInvoiced = item.paidDate !== null;

            // Find or create client entry for this month
            let clientEntry = monthlyData[monthIndex].clientRevenue.find(
                (c) => c.clientName === item.clientName
            );

            if (!clientEntry) {
                clientEntry = {
                    clientName: item.clientName,
                    sumInvoiced: 0,
                    sumPending: 0,
                };
                monthlyData[monthIndex].clientRevenue.push(clientEntry);
            }

            // Update client-specific amounts
            if (isInvoiced) {
                clientEntry.sumInvoiced += item.gross_amount;
                monthlyData[monthIndex].sumInvoiced += item.gross_amount;
            } else {
                clientEntry.sumPending += item.gross_amount;
                monthlyData[monthIndex].sumPending += item.gross_amount;
            }
        });

        // Step 3: Calculate cumulative values
        let cumulativeInvoiced = 0;
        let cumulativePending = 0;

        monthlyData.forEach((monthlyData) => {
            cumulativeInvoiced += monthlyData.sumInvoiced;
            cumulativePending += monthlyData.sumPending;
            monthlyData.accumulatedInvoiced = cumulativeInvoiced;
            monthlyData.accumulatedPending = cumulativePending;
        });

        return monthlyData;
    };

    const areaChartData = convertDataToChartFormat(data, year);
    console.log("Area Chart Data:", areaChartData);

    return (
        <Card className="pt-0">
            <CardHeader className="flex items-center gap-2 space-y-0 py-5 sm:flex-row">
                <div className="grid flex-1 gap-1">
                    <CardTitle>Revenue</CardTitle>
                    <CardDescription>Cumulative yearly revenue</CardDescription>
                </div>
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
            </CardHeader>
            <CardContent className="px-2 pt-4 sm:px-6 sm:pt-6">
                <ChartContainer
                    config={chartConfig}
                    className="aspect-auto h-[250px] w-full"
                >
                    <ComposedChart data={areaChartData}>
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
                                    stopOpacity={0.4}
                                />
                                <stop
                                    offset="95%"
                                    stopColor="var(--color-invoiced)"
                                    stopOpacity={0.05}
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
                                    stopOpacity={0.4}
                                />
                                <stop
                                    offset="95%"
                                    stopColor="var(--color-pending)"
                                    stopOpacity={0.05}
                                />
                            </linearGradient>
                        </defs>
                        <CartesianGrid vertical={false} />
                        <XAxis
                            dataKey="month"
                            tickLine={false}
                            axisLine={false}
                            tickMargin={8}
                            minTickGap={32}
                            tickFormatter={(value) => {
                                const date = new Date(year, value);
                                return date.toLocaleDateString("en-EU", {
                                    month: "short",
                                });
                            }}
                        />
                        <YAxis
                            tickLine={false}
                            axisLine={false}
                            tickMargin={10}
                        />
                        <ChartTooltip
                            cursor={false}
                            content={
                                <ChartTooltipContent
                                    labelKey="clientRevenue"
                                    indicator="line"
                                    hideLabel={false}
                                    labelFormatter={(value) => {
                                        return new Date(
                                            value
                                        ).toLocaleDateString("en-EU", {
                                            month: "long",
                                            year: "numeric",
                                        });
                                    }}
                                />
                            }
                        />
                        <Area
                            dataKey="accumulatedInvoiced"
                            type="monotone"
                            fill="url(#filInvoiced)"
                            stroke="var(--color-invoiced)"
                            strokeWidth={2}
                            stackId="a"
                            activeDot={false}
                        />
                        <Area
                            dataKey="accumulatedPending"
                            type="monotone"
                            fill="url(#fillPending)"
                            stroke="var(--color-pending)"
                            strokeWidth={2}
                            stackId="a"
                            activeDot={false}
                        />
                        <Bar
                            dataKey="sumInvoiced"
                            fill="var(--color-invoiced)"
                            fillOpacity={0.2}
                            stackId="b"
                            radius={[10, 10, 0, 0]}
                        />
                        <Bar
                            dataKey="sumPending"
                            fill="var(--color-pending)"
                            fillOpacity={0.3}
                            stackId="b"
                            radius={[10, 10, 0, 0]}
                        />
                    </ComposedChart>
                </ChartContainer>
            </CardContent>
        </Card>
    );
}

export default RevenueChart;
