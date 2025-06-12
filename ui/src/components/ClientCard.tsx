import { AppCard } from "./AppCard";

interface ClientCardProps {
    client_name: string;
    totalInvoiceNumber: number;
    totalInvoiceAmount: number;
    totalInvoiceAmountCurrency: string;
}

function ClientCard({
    client_name,
    totalInvoiceNumber,
    totalInvoiceAmount,
    totalInvoiceAmountCurrency,
}: ClientCardProps) {
    return (
        <>
            <AppCard>
                <h3>{client_name}</h3>
                <div className="flex justify-between flex-nowrap">
                    <div className="flex w-3/8 space-x-8 justify-start">
                        <p className="flex italic font-semibold text-sm">
                            {totalInvoiceNumber} invoices
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
