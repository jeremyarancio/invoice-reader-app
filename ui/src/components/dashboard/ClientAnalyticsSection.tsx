import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { CURRENCIES } from "@/schemas/invoice";
import type { Currency } from "@/stores/currencyStore";
import type { TopClient } from "@/lib/utils/dashboardCalculations";
import { TrendingUp, FileText, ArrowRight } from "lucide-react";
import { useNavigate } from "react-router-dom";

interface ClientAnalyticsSectionProps {
  clients: TopClient[];
  currency: Currency;
  totalClients: number;
}

export function ClientAnalyticsSection({
  clients,
  currency,
  totalClients,
}: ClientAnalyticsSectionProps) {
  const navigate = useNavigate();
  const currencySymbol = CURRENCIES[currency]?.symbol || currency;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Top Clients by Revenue</CardTitle>
      </CardHeader>
      <CardContent>
        {clients.length === 0 ? (
          <div className="text-center py-8 text-muted-foreground">
            <p>No client data available for {currency}</p>
          </div>
        ) : (
          <div className="space-y-3">
            {clients.map((client, index) => (
              <div
                key={client.clientId}
                className="flex items-center justify-between p-3 rounded-lg transition-colors hover:bg-muted/50 cursor-pointer"
                onClick={() => navigate(`/clients/${client.clientId}`)}
              >
                <div className="flex items-center gap-3 flex-1 min-w-0">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                    <span className="text-sm font-semibold text-primary">
                      {index + 1}
                    </span>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-medium truncate">{client.clientName}</p>
                    <p className="text-sm text-muted-foreground flex items-center gap-1">
                      <FileText className="h-3 w-3" />
                      {client.invoiceCount} invoice{client.invoiceCount !== 1 ? "s" : ""}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <div className="text-right">
                    <p className="font-semibold whitespace-nowrap">
                      {currencySymbol}
                      {client.revenue.toLocaleString("en-US", {
                        minimumFractionDigits: 0,
                        maximumFractionDigits: 0,
                      })}
                    </p>
                  </div>
                  <TrendingUp className="h-4 w-4 text-green-500" />
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
      <CardFooter className="border-t">
        <Button
          variant="ghost"
          className="w-full"
          onClick={() => navigate("/clients")}
        >
          View All {totalClients} Clients
          <ArrowRight className="ml-2 h-4 w-4" />
        </Button>
      </CardFooter>
    </Card>
  );
}
