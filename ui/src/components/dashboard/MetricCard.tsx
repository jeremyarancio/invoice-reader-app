import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CURRENCIES } from "@/schemas/invoice";
import type { Currency } from "@/stores/currencyStore";
import { cn } from "@/lib/utils";
import type { LucideIcon } from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: LucideIcon;
  currency?: Currency;
  colorScheme?: "default" | "success" | "warning" | "danger";
  className?: string;
}

const colorSchemes = {
  default: "border-border",
  success: "border-green-500/50 bg-green-50/50 dark:bg-green-950/20",
  warning: "border-yellow-500/50 bg-yellow-50/50 dark:bg-yellow-950/20",
  danger: "border-red-500/50 bg-red-50/50 dark:bg-red-950/20",
};

export function MetricCard({
  title,
  value,
  subtitle,
  icon: Icon,
  currency,
  colorScheme = "default",
  className,
}: MetricCardProps) {
  const formatValue = () => {
    if (typeof value === "number" && currency) {
      const currencySymbol = CURRENCIES[currency]?.symbol || currency;
      return `${currencySymbol}${value.toLocaleString("en-US", {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
      })}`;
    }
    return value;
  };

  return (
    <Card className={cn(colorSchemes[colorScheme], className)}>
      <CardHeader>
        <div className="flex items-start justify-between">
          <CardTitle className="text-sm font-medium text-muted-foreground">
            {title}
          </CardTitle>
          {Icon && (
            <Icon className="h-4 w-4 text-muted-foreground" />
          )}
        </div>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{formatValue()}</div>
        {subtitle && (
          <p className="text-xs text-muted-foreground mt-1">{subtitle}</p>
        )}
      </CardContent>
    </Card>
  );
}
