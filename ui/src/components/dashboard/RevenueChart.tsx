import {
    ComposedChart,
    Area,
    CartesianGrid,
    XAxis,
    YAxis,
    Bar,
    type TooltipProps,
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
} from "@/components/ui/chart";
import { useCurrencyStore } from "@/stores/currencyStore";
import { CURRENCIES } from "@/schemas/invoice";

export type MonthlyChartData = {
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

interface RevenueChartProps {
    data: MonthlyChartData[];
}

const ChartToolTip = ({
    active,
    payload,
}: TooltipProps<string | number, string>) => {
    if (!active || !payload) return null;

    const monthData = payload[0].payload as MonthlyChartData;
    const { selectedCurrency } = useCurrencyStore();

    // Only show tooltip for months with invoices
    if (monthData.clientRevenue.length === 0) {
        return null;
    }

    return (
        <div className="rounded-lg border bg-background p-3 shadow-sm">
            <div className="space-y-2">
                {monthData.clientRevenue.map((client) => (
                    <div key={client.clientName} className="space-y-1">
                        <div className="font-medium text-base">
                            {client.clientName}
                        </div>
                        <div className="text-sm">
                            {client.sumInvoiced > 0 && (
                                <div className="flex items-center gap-1">
                                    <div
                                        className="h-2 w-2 rounded-full"
                                        style={{
                                            backgroundColor:
                                                "var(--color-invoiced)",
                                        }}
                                    />
                                    <span>
                                        Invoiced: {CURRENCIES[selectedCurrency]?.symbol}
                                        {client.sumInvoiced.toLocaleString("en-US", {
                                            minimumFractionDigits: 0,
                                            maximumFractionDigits: 0,
                                        })}
                                    </span>
                                </div>
                            )}
                            {client.sumPending > 0 && (
                                <div className="flex items-center gap-1">
                                    <div
                                        className="h-2 w-2 rounded-full"
                                        style={{
                                            backgroundColor:
                                                "var(--color-pending)",
                                        }}
                                    />
                                    <span>
                                        Pending: {CURRENCIES[selectedCurrency]?.symbol}
                                        {client.sumPending.toLocaleString("en-US", {
                                            minimumFractionDigits: 0,
                                            maximumFractionDigits: 0,
                                        })}
                                    </span>
                                </div>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

function RevenueChart({ data }: RevenueChartProps) {
    return (
        <Card className="pt-0">
            <CardHeader className="flex items-center gap-2 space-y-0 py-5 sm:flex-row">
                <div className="grid flex-1 gap-1">
                    <CardTitle>Revenue</CardTitle>
                    <CardDescription>Cumulative yearly revenue</CardDescription>
                </div>
            </CardHeader>
            <CardContent className="px-2 pt-4 sm:px-6 sm:pt-6">
                <ChartContainer
                    config={chartConfig}
                    className="aspect-auto h-[250px] w-full"
                >
                    <ComposedChart data={data}>
                        <defs>
                            <linearGradient
                                id="fillInvoiced"
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
                            minTickGap={20}
                            tickFormatter={(value) => {
                                const date = new Date(2025, value - 1);
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
                        <ChartTooltip content={<ChartToolTip />} />
                        <Area
                            dataKey="accumulatedInvoiced"
                            type="monotone"
                            fill="url(#fillInvoiced)"
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
                            fillOpacity={0.3}
                            stackId="b"
                            radius={[10, 10, 0, 0]}
                            isAnimationActive={true}
                            activeBar={{
                                fill: "var(--color-invoiced)",
                                fillOpacity: 0.8,
                                stroke: "var(--color-invoiced)",
                                strokeWidth: 2,
                                strokeOpacity: 0.9,
                            }}
                        />
                        <Bar
                            dataKey="sumPending"
                            fill="var(--color-pending)"
                            fillOpacity={0.3}
                            stackId="b"
                            radius={[10, 10, 0, 0]}
                            isAnimationActive={true}
                            activeBar={{
                                fill: "var(--color-pending)",
                                fillOpacity: 0.8,
                                stroke: "var(--color-pending)",
                                strokeWidth: 2,
                                strokeOpacity: 0.9,
                            }}
                        />
                    </ComposedChart>
                </ChartContainer>
            </CardContent>
        </Card>
    );
}

export default RevenueChart;
