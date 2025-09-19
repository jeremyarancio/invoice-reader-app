import {
    useFetchInvoice,
    useFetchInvoiceUrl,
} from "@/hooks/api/invoice";
import { useNavigate, useParams } from "react-router-dom";
import { useFetchClients } from "@/hooks/api/client";
import PdfPreview from "@/components/PdfPreview";
import { ArrowLeft } from "lucide-react";
import ViewInvoiceForm from "@/components/ViewInvoiceForm";

function ViewInvoice() {
    const { invoiceId } = useParams();
    const navigate = useNavigate();

    const { invoice, isLoading: isInvoiceLoading } = useFetchInvoice(invoiceId);
    const { clients, isLoading: isClientsLoading } = useFetchClients();
    const { url: invoiceUrl } = useFetchInvoiceUrl(invoiceId);

    console.log("Invoice URL:", invoiceUrl);

    return (
        <>
            <div className="mt-10 ml-10">
                <button
                    onClick={() => navigate("/invoices")}
                    className="hover:cursor-pointer"
                >
                    <ArrowLeft
                        size={40}
                        className="rounded-full hover:bg-stone-50"
                    />
                </button>
            </div>
            <h1 className="text-2xl font-bold ml-20 my-10">Invoice Details</h1>

            <div className="grid grid-cols-5 mt-20 mb-40">
                <div className="col-span-3 flex justify-center">
                    {invoiceUrl && (
                        <div className="px-4 ">
                            <PdfPreview file={invoiceUrl} />
                        </div>
                    )}
                </div>
                <div className="col-span-2 md:px-20 w-full">
                    {!isInvoiceLoading &&
                        !isClientsLoading &&
                        !!invoice && (
                            <ViewInvoiceForm
                                invoice={invoice}
                                clients={clients}
                            />
                        )}
                </div>
            </div>
        </>
    );
}

export default ViewInvoice;
