import { useNavigate } from "react-router-dom";
import { AppCard } from "./AppCard";
import { useDeleteClient } from "@/hooks/api/client";

interface ClientCardProps {
    clientId: string;
    clientName: string;
    totalInvoice: number;
    totalInvoiceAmount: number;
    totalInvoiceAmountCurrency: string;
}

function ClientCard({
    clientId,
    clientName,
    totalInvoice,
    totalInvoiceAmount,
    totalInvoiceAmountCurrency,
}: ClientCardProps) {
    const navigate = useNavigate();
    const deleteClient = useDeleteClient();

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
                        <div className="font-semibold">
                            <span className="flex font-semibold">
                                {totalInvoiceAmount}{" "}
                                {totalInvoiceAmountCurrency}
                            </span>
                        </div>
                        <div className="my-auto w-1/30"></div>
                    </div>
                </div>
            </AppCard>
        </>
    );
}

export default ClientCard;
