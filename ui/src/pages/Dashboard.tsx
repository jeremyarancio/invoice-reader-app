import { useDashboardData } from "@/hooks/useDashboardData";
import { useCurrencyStore } from "@/stores/currencyStore";
import { DashboardHeader } from "@/components/dashboard/DashboardHeader";
import { MetricCard } from "@/components/dashboard/MetricCard";
import { ClientAnalyticsSection } from "@/components/dashboard/ClientAnalyticsSection";
import { QuickActionsSection } from "@/components/dashboard/QuickActionsSection";
import { Skeleton } from "@/components/ui/skeleton";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { DollarSign, FileText, Clock, AlertTriangle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import RevenueChart from "@/components/dashboard/RevenueChart";

export default function Dashboard() {
    const { selectedCurrency } = useCurrencyStore();
    const { metrics, isLoading, error, hasData } = useDashboardData();
    const navigate = useNavigate();

    if (isLoading) {
        return (
            <div className="max-w-7xl mx-auto px-4 py-8">
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
                    <div>
                        <Skeleton className="h-9 w-48 mb-2" />
                        <Skeleton className="h-5 w-96" />
                    </div>
                    <Skeleton className="h-8 w-40" />
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                    {[...Array(4)].map((_, i) => (
                        <Card key={i}>
                            <CardHeader>
                                <Skeleton className="h-4 w-24" />
                            </CardHeader>
                            <CardContent>
                                <Skeleton className="h-8 w-32 mb-2" />
                                <Skeleton className="h-3 w-20" />
                            </CardContent>
                        </Card>
                    ))}
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <Card>
                        <CardHeader>
                            <Skeleton className="h-6 w-32" />
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-4">
                                {[...Array(3)].map((_, i) => (
                                    <Skeleton key={i} className="h-16 w-full" />
                                ))}
                            </div>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <Skeleton className="h-6 w-40" />
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-3">
                                {[...Array(5)].map((_, i) => (
                                    <Skeleton key={i} className="h-14 w-full" />
                                ))}
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        );
    }

    // Error state
    if (error) {
        return (
            <div className="max-w-7xl mx-auto px-4 py-8">
                <DashboardHeader currency={selectedCurrency} />
                <div className="flex flex-col items-center justify-center py-16 text-center">
                    <AlertTriangle className="h-16 w-16 text-destructive mb-4" />
                    <h2 className="text-2xl font-bold mb-2">
                        Error Loading Dashboard
                    </h2>
                    <p className="text-muted-foreground mb-6">
                        There was an error loading your dashboard data. Please
                        try again.
                    </p>
                    <Button onClick={() => window.location.reload()}>
                        Retry
                    </Button>
                </div>
            </div>
        );
    }

    if (!hasData || !metrics) {
        return (
            <div className="max-w-7xl mx-auto px-4 py-8">
                <DashboardHeader currency={selectedCurrency} />
                <div className="flex flex-col items-center justify-center py-16 text-center">
                    <FileText className="h-16 w-16 text-muted-foreground mb-4" />
                    <h2 className="text-2xl font-bold mb-2">
                        Welcome to Your Dashboard
                    </h2>
                    <p className="text-muted-foreground mb-6 max-w-md">
                        You haven't added any invoices yet. Get started by
                        uploading your first invoice or adding a client.
                    </p>
                    <div className="flex gap-4">
                        <Button onClick={() => navigate("/invoices/add")}>
                            Add Your First Invoice
                        </Button>
                        <Button
                            variant="outline"
                            onClick={() => navigate("/clients/add")}
                        >
                            Add a Client
                        </Button>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-7xl mx-auto px-4 py-8">
            <DashboardHeader currency={selectedCurrency} />

            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                <MetricCard
                    title="Total Revenue"
                    value={metrics.totalRevenue}
                    currency={selectedCurrency}
                    icon={DollarSign}
                    colorScheme="default"
                />
                <MetricCard
                    title="Pending Payments"
                    value={metrics.pendingAmount}
                    subtitle={`${metrics.unpaidInvoices} invoice${
                        metrics.unpaidInvoices !== 1 ? "s" : ""
                    }`}
                    currency={selectedCurrency}
                    icon={Clock}
                    colorScheme="warning"
                />
            </div>

            <div className="flex flex-col gap-6 mb-8">
                <RevenueChart />

                <ClientAnalyticsSection
                    clients={metrics.topClients}
                    currency={selectedCurrency}
                    totalClients={metrics.topClients.length}
                />
            </div>

            <QuickActionsSection />
        </div>
    );
}
