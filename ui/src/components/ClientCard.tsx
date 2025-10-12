import { useNavigate } from "react-router-dom";
import { AppCard } from "./AppCard";
import { useDeleteClient } from "@/hooks/api/client";
import { useCurrencyStore } from "@/stores/currencyStore";

interface ClientCardProps {
    clientId: string;
    clientName: string;
    totalInvoice: number;
    totalRevenue: Record<string, number>;
}

function ClientCard({
    clientId,
    clientName,
    totalInvoice,
    totalRevenue,
}: ClientCardProps) {
    const navigate = useNavigate();
    const deleteClient = useDeleteClient();
    const { selectedCurrency } = useCurrencyStore();

    return (
        <>
            <AppCard
                onClick={() => navigate(`/clients/${clientId}`)}
                onEdit={() => navigate(`/clients/${clientId}`)}
                onDelete={() => deleteClient(clientId)}
            >
                <h3>{clientName}</h3>
                <div className="flex justify-between flex-nowrap">
                    <div className="flex w-3/8 space-x-8 justify-start">
                        <p className="flex italic font-semibold text-sm">
                            {totalInvoice} invoices
                        </p>
                    </div>
                    <div className="w-3/8"></div>
                    <div className="flex w-2/8 space-x-8 justify-evenly">
                        <div className="font-semibold text-right">
                            {totalRevenue?.[selectedCurrency]?.toFixed(2) || '0.00'} {selectedCurrency}
                        </div>
                        <div className="my-auto w-1/30"></div>
                    </div>
                </div>
            </AppCard>
        </>
    );
}

export default ClientCard;
