import { AppCard } from "@/components/AppCard";
import { format } from "date-fns";
import { useNavigate } from "react-router-dom";

interface InvoiceCardProps {
    invoiceId: string;
    invoiceDescription: string;
    grossAmount: number;
    invoiceNumber: string;
    issuedDate: Date;
    status: "paid" | "unpaid" | "overdue";
    currency?: string;
}

function InvoiceCard({
    invoiceId,
    invoiceDescription,
    grossAmount,
    invoiceNumber,
    issuedDate,
    status,
    currency,
}: InvoiceCardProps) {
    const navigate = useNavigate();

    return (
        <>
            <AppCard onEdit={() => navigate(`/invoices/${invoiceId}`)}>
                <h3>{invoiceDescription}</h3>
                <div className="flex justify-between flex-nowrap">
                    <div className="flex w-3/8 space-x-8 justify-start">
                        <p className="flex italic font-semibold">
                            N° {invoiceNumber}
                        </p>
                        <p className="flex font-semibold">
                            {format(issuedDate, "dd/MM/yyyy")}
                        </p>
                    </div>
                    <div className="w-3/8"></div>
                    <div className="flex w-2/8 space-x-8 justify-evenly">
                        <p
                            className={`${
                                status === "paid"
                                    ? "text-green-500"
                                    : status === "unpaid"
                                    ? "text-yellow-500"
                                    : "text-red-500"
                            } font-semibold`}
                        >
                            {status === "paid"
                                ? "Paid"
                                : status === "unpaid"
                                ? "Unpaid"
                                : "Overdue"}
                        </p>
                        <p className="font-semibold">
                            {grossAmount} {currency}
                        </p>
                    </div>
                </div>
            </AppCard>
        </>
    );
}

export default InvoiceCard;
