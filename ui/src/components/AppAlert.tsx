import { Check, AlertCircle, Info, AlertTriangle, X } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { useAlert } from "@/contexts/AlertContext";

const iconMap = {
    success: Check,
    error: AlertCircle,
    warning: AlertTriangle,
    info: Info,
};

function AppAlert() {
    const { alerts, dismissAlert } = useAlert();

    if (alerts.length === 0) return null;

    return (
        <div className="fixed bottom-3 right-10 z-50 space-y-2">
            {alerts.map((alert) => {
                const Icon = iconMap[alert.type];
                return (
                    <Alert
                        key={alert.id}
                        className="w-96 flex items-start shadow-lg animate-in slide-in-from-right"
                        variant={alert.type === 'error' ? 'destructive' : 'default'}
                    >
                        <Icon className="h-4 w-4" />
                        <div className="flex-1">
                            <AlertTitle>{alert.title}</AlertTitle>
                            <AlertDescription>{alert.message}</AlertDescription>
                        </div>
                        <button
                            className="ml-2"
                            onClick={() => dismissAlert(alert.id)}
                        >
                            <X className="h-4 w-4" />
                        </button>
                    </Alert>
                );
            })}
        </div>
    );
}

export default AppAlert;
