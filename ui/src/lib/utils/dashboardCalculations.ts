import type { Invoice } from "@/schemas/invoice";
import type { Client } from "@/schemas/client";

export type InvoiceStatus = "paid" | "unpaid" | "overdue";

export interface DashboardMetrics {
    totalRevenue: number;
    totalInvoices: number;
    paidInvoices: number;
    unpaidInvoices: number;
    overdueInvoices: number;
    pendingAmount: number;
    overdueAmount: number;
    topClients: TopClient[];
    paymentStatusBreakdown: PaymentStatusBreakdown;
}

export interface TopClient {
    clientId: string;
    clientName: string;
    revenue: number;
    invoiceCount: number;
}

export interface PaymentStatusBreakdown {
    paid: {
        count: number;
        amount: number;
        percentage: number;
    };
    unpaid: {
        count: number;
        amount: number;
        percentage: number;
    };
    overdue: {
        count: number;
        amount: number;
        percentage: number;
    };
}

const PAYMENT_TERM_DAYS = 30;

export function getInvoiceStatus(invoice: Invoice): InvoiceStatus {
    if (invoice.paidDate) return "paid";

    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - PAYMENT_TERM_DAYS);

    if (invoice.issuedDate < thirtyDaysAgo) return "overdue";

    return "unpaid";
}

export function filterInvoicesByCurrency(
    invoices: Invoice[],
    currency: string
): Invoice[] {
    return invoices.filter((invoice) => invoice.currency === currency);
}

export function calculateTotalRevenue(invoices: Invoice[]): number {
    return invoices.reduce((sum, invoice) => sum + invoice.grossAmount, 0);
}

export function calculatePaymentStatusBreakdown(
    invoices: Invoice[]
): PaymentStatusBreakdown {
    const totalInvoices = invoices.length;

    const breakdown = invoices.reduce(
        (acc, invoice) => {
            const status = getInvoiceStatus(invoice);
            acc[status].count++;
            acc[status].amount += invoice.grossAmount;
            return acc;
        },
        {
            paid: { count: 0, amount: 0, percentage: 0 },
            unpaid: { count: 0, amount: 0, percentage: 0 },
            overdue: { count: 0, amount: 0, percentage: 0 },
        }
    );

    // Calculate percentages
    if (totalInvoices > 0) {
        breakdown.paid.percentage =
            (breakdown.paid.count / totalInvoices) * 100;
        breakdown.unpaid.percentage =
            (breakdown.unpaid.count / totalInvoices) * 100;
        breakdown.overdue.percentage =
            (breakdown.overdue.count / totalInvoices) * 100;
    }

    return breakdown;
}

export function calculateTopClients(
    invoices: Invoice[],
    clients: Client[],
    limit: number = 5
): TopClient[] {
    // Create a map of client revenue from invoices
    const clientRevenueMap = new Map<
        string,
        { revenue: number; count: number }
    >();

    invoices.forEach((invoice) => {
        const existing = clientRevenueMap.get(invoice.clientId) || {
            revenue: 0,
            count: 0,
        };
        clientRevenueMap.set(invoice.clientId, {
            revenue: existing.revenue + invoice.grossAmount,
            count: existing.count + 1,
        });
    });

    // Create client lookup map
    const clientMap = new Map<string, Client>();
    clients.forEach((client) => {
        clientMap.set(client.id, client);
    });

    // Convert to TopClient array
    const topClients: TopClient[] = [];
    clientRevenueMap.forEach((data, clientId) => {
        const client = clientMap.get(clientId);
        if (client) {
            topClients.push({
                clientId,
                clientName: client.clientName,
                revenue: data.revenue,
                invoiceCount: data.count,
            });
        }
    });

    // Sort by revenue descending and limit
    return topClients.sort((a, b) => b.revenue - a.revenue).slice(0, limit);
}

/**
 * Main function to calculate all dashboard metrics
 */
export function calculateDashboardMetrics(
    invoices: Invoice[],
    clients: Client[],
    selectedCurrency: string
): DashboardMetrics {
    // Filter invoices by selected currency
    const currencyInvoices = filterInvoicesByCurrency(
        invoices,
        selectedCurrency
    );

    // Calculate payment status breakdown
    const paymentStatusBreakdown =
        calculatePaymentStatusBreakdown(currencyInvoices);

    // Calculate totals
    const totalRevenue = calculateTotalRevenue(currencyInvoices);
    const totalInvoices = currencyInvoices.length;

    // Calculate top clients
    const topClients = calculateTopClients(currencyInvoices, clients, 5);

    return {
        totalRevenue,
        totalInvoices,
        paidInvoices: paymentStatusBreakdown.paid.count,
        unpaidInvoices: paymentStatusBreakdown.unpaid.count,
        overdueInvoices: paymentStatusBreakdown.overdue.count,
        pendingAmount: paymentStatusBreakdown.unpaid.amount,
        overdueAmount: paymentStatusBreakdown.overdue.amount,
        topClients,
        paymentStatusBreakdown,
    };
}
