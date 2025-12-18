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

type RawData = {
    clientName: string;
    grossAmount: number;
    issuedDate: Date;
    paidDate?: Date;
};

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
    data: RawData[];
    year: string;
}

const convertDataToChartFormat = (
    data: RawData[],
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
    data.forEach((item) => {
        const date = item.paidDate || item.issuedDate;
        if (date.getFullYear() !== year) return;

        const monthIndex = date.getMonth();
        const isInvoiced = !!item.paidDate;

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
            clientEntry.sumInvoiced += item.grossAmount;
            monthlyData[monthIndex].sumInvoiced += item.grossAmount;
        } else {
            clientEntry.sumPending += item.grossAmount;
            monthlyData[monthIndex].sumPending += item.grossAmount;
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

const ChartToolTip = ({
    active,
    payload,
}: TooltipProps<string | number, string>) => {
    if (!active || !payload) return null;

    const monthData = payload[0].payload as MonthlyChartData;

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
                                        Invoiced: $
                                        {client.sumInvoiced.toString()}
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
                                        Pending: ${client.sumPending.toString()}
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

function RevenueChart({ data, year }: RevenueChartProps) {
    const areaChartData = convertDataToChartFormat(data, parseInt(year));

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
                            minTickGap={20}
                            tickFormatter={(value) => {
                                const date = new Date(parseInt(year), value);
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
