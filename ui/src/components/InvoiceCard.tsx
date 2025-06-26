import { AppCard } from "@/components/AppCard";
import { useDeleteInvoice } from "@/hooks/api/invoice";
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
    clientName: string;
}

function InvoiceCard({
    invoiceId,
    invoiceDescription,
    grossAmount,
    invoiceNumber,
    issuedDate,
    status,
    currency,
    clientName,
}: InvoiceCardProps) {
    const navigate = useNavigate();
    const deleteInvoice = useDeleteInvoice();

    return (
        <>
            <AppCard
                onClick={() => navigate(`/invoices/${invoiceId}`)}
                onEdit={() => navigate(`/invoices/${invoiceId}`)}
                onDelete={() => deleteInvoice(invoiceId)}
            >
                <h3>{invoiceDescription}</h3>
                <div className="flex justify-between items-center mr-4">
                    <div className="flex flex-none gap-8 justify-start">
                        <p className="italic font-semibold whitespace-nowrap">
                            {invoiceNumber}
                        </p>
                        <p className="whitespace-nowrap">
                            {format(issuedDate, "dd/MM/yyyy")}
                        </p>
                        <p className="italic font-semibold whitespace-nowrap">
                            {clientName}
                        </p>
                    </div>
                    <div className="flex flex-initial gap-4 justify-end items-center">
                        <p
                            className={`${
                                status === "paid"
                                    ? "text-green-500"
                                    : status === "unpaid"
                                    ? "text-yellow-500"
                                    : "text-red-500"
                            } font-semibold whitespace-nowrap`}
                        >
                            {status === "paid"
                                ? "Paid"
                                : status === "unpaid"
                                ? "Unpaid"
                                : "Overdue"}
                        </p>
                        <p className="font-semibold whitespace-nowrap">
                            {grossAmount} {currency}
                        </p>
                    </div>
                </div>
            </AppCard>
        </>
    );
}

export default InvoiceCard;
