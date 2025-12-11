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
        paidDate: new Date("2024-03-05"),
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

const CustomBar = (props: any) => {
    const { fill, x, y, width, height, payload, fillOpacity } = props;

    // Only render bar if there's actual monthly invoiced or pending data
    if (payload.monthlyInvoiced === 0 && payload.monthlyPending === 0) {
        return null;
    }

    return (
        <rect
            x={x}
            y={y}
            width={width}
            height={height}
            fill={fill}
            fillOpacity={fillOpacity || 1}
        />
    );
};

const CustomActiveBar = (props: any) => {
    const { fill, x, y, width, payload, height, stroke, strokeWidth } = props;

    // Only render active bar if there's actual monthly invoiced or pending data
    if (payload.monthlyInvoiced === 0 && payload.monthlyPending === 0) {
        return null;
    }

    return (
        <rect
            x={x}
            y={y}
            width={width}
            height={height}
            fill={fill}
            fillOpacity={0.6}
            stroke={stroke}
            strokeWidth={strokeWidth || 2}
        />
    );
};

function RevenueChart() {
    const availableYears = Array.from(
        new Set(data.map((item) => new Date(item.issuedDate).getFullYear()))
    ).sort((a, b) => b - a);

    const [selectedYear, setSelectedYear] = useState(
        availableYears[0]?.toString() || new Date().getFullYear().toString()
    );

    const year = parseInt(selectedYear);

    const convertDataToAreaChartFormat = (d: typeof data) => {
        const chartData = d.map((item) => {
            return {
                date: item.paidDate || item.issuedDate,
                invoiced: item.paidDate ? item.gross_amount : 0,
                pending: item.paidDate ? 0 : item.gross_amount,
            };
        });

        const generateYearMonths = () => {
            const months = [];
            for (let month = 0; month < 12; month++) {
                months.push({
                    month: month,
                    invoiced: 0,
                    pending: 0,
                });
            }
            return months;
        };

        const aggregateByMonth = (data: typeof chartData) => {
            const yearMonths = generateYearMonths();

            data.forEach((item) => {
                if (item.date.getFullYear() === year) {
                    const monthIndex = item.date.getMonth();
                    yearMonths[monthIndex].invoiced += item.invoiced;
                    yearMonths[monthIndex].pending += item.pending;
                }
            });

            return yearMonths;
        };

        const calculateCumulative = (
            data: ReturnType<typeof aggregateByMonth>
        ) => {
            let cumulativeInvoiced = 0;
            let cumulativePending = 0;

            return data.map((item) => {
                cumulativeInvoiced += item.invoiced;
                cumulativePending += item.pending;

                return {
                    ...item,
                    monthlyInvoiced: item.invoiced,
                    monthlyPending: item.pending,
                    invoiced: cumulativeInvoiced,
                    pending: cumulativePending,
                };
            });
        };

        return calculateCumulative(aggregateByMonth(chartData));
    };

    const areaChartData = convertDataToAreaChartFormat(data);

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
                            dataKey="date"
                            tickLine={false}
                            axisLine={false}
                            tickMargin={8}
                            minTickGap={32}
                            tickFormatter={(value) => {
                                const date = new Date(value);
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
                                    indicator="line"
                                    labelFormatter={(value) => {
                                        return new Date(
                                            value
                                        ).toLocaleDateString("en-EU", {
                                            month: "long",
                                            year: "numeric",
                                        });
                                    }}
                                    formatter={(value, name, item) => {
                                        if (
                                            item.payload.monthlyInvoiced ===
                                                0 &&
                                            item.payload.monthlyPending === 0
                                        ) {
                                            return null;
                                        }
                                        return (
                                            <div className="flex flex-col gap-1">
                                                {item.payload.clientName && (
                                                    <span className="text-xs text-muted-foreground">
                                                        {
                                                            item.payload
                                                                .clientName
                                                        }
                                                    </span>
                                                )}
                                                <span>
                                                    {name}: $
                                                    {Number(
                                                        value
                                                    ).toLocaleString()}
                                                </span>
                                            </div>
                                        );
                                    }}
                                />
                            }
                        />
                        <Area
                            dataKey="invoiced"
                            type="monotone"
                            fill="url(#filInvoiced)"
                            stroke="var(--color-invoiced)"
                            strokeWidth={2}
                            stackId="a"
                            activeDot={false}
                        />
                        <Area
                            dataKey="pending"
                            type="monotone"
                            fill="url(#fillPending)"
                            stroke="var(--color-pending)"
                            strokeWidth={2}
                            stackId="a"
                            activeDot={false}
                        />
                        <Bar
                            dataKey="invoiced"
                            fill="var(--color-invoiced)"
                            fillOpacity={0.3}
                            stackId="b"
                            radius={[0, 0, 0, 0]}
                            shape={CustomBar}
                            activeBar={
                                <CustomActiveBar stroke="var(--color-invoiced)" />
                            }
                        />
                        <Bar
                            dataKey="pending"
                            fill="var(--color-pending)"
                            fillOpacity={0.3}
                            stackId="b"
                            radius={[0, 4, 0, 0]}
                            shape={CustomBar}
                            activeBar={
                                <CustomActiveBar stroke="var(--color-pending)" />
                            }
                        />
                    </ComposedChart>
                </ChartContainer>
            </CardContent>
        </Card>
    );
}

export default RevenueChart;
