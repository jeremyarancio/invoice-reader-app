import {
    useFetchCurrencies,
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
    const { currencies, isLoading: isCurrenciesLoading } = useFetchCurrencies();
    const { clients, isLoading: isClientsLoading } = useFetchClients();

    const { url: invoiceUrl } = useFetchInvoiceUrl(invoiceId);

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

            <div className="flex mt-20 mb-40 justify-around">
                {invoiceUrl && (
                    <div className="px-4 flex justify-center">
                        <PdfPreview file={invoiceUrl} />
                    </div>
                )}
                <div className="px-4 md:px-20 w-full">
                    {!isInvoiceLoading &&
                        !isCurrenciesLoading &&
                        !isClientsLoading &&
                        !!invoice && (
                            <ViewInvoiceForm
                                invoice={invoice}
                                clients={clients}
                                currencies={currencies}
                            />
                        )}
                </div>
            </div>
        </>
    );
}

export default ViewInvoice;
