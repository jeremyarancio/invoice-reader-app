import { ArrowLeft } from "lucide-react";

import { useNavigate, useLocation } from "react-router-dom";
import PdfPreview from "@/components/PdfPreview";
import {
    useFetchCurrencies,
    useParseInvoiceMutation,
} from "@/hooks/api/invoice";
import { useFetchClients } from "@/hooks/api/client";
import AddInvoiceForm from "@/components/AddInvoiceForm";
import { useEffect } from "react";

function AddInvoice() {
    const navigate = useNavigate();
    const file: File = useLocation().state?.file;
    const { clients } = useFetchClients();
    const { currencies } = useFetchCurrencies();
    const parseInvoiceMutation = useParseInvoiceMutation();

    useEffect(() => {
        if (file && !parseInvoiceMutation.isPending) {
            const hasRunRef = { current: false }; // Necessary to avoid double call
            if (!hasRunRef.current) {
                hasRunRef.current = true;
                parseInvoiceMutation.mutate(file);
            }
        }
    }, [file]);

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
            <div className="flex mt-20 mb-40 justify-around">
                <div className="px-4 flex justify-center">
                    <PdfPreview file={file} />
                </div>
                <div className="px-4 md:px-20 w-full">
                    {parseInvoiceMutation.isPending && (
                        <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                            <div className="flex items-center space-x-3">
                                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
                                <span className="text-blue-700 font-medium">
                                    Parsing invoice document...
                                </span>
                            </div>
                            <p className="text-blue-600 text-sm mt-1">
                                Extracting information from your document. This
                                may take a few moments.
                            </p>
                        </div>
                    )}
                    {parseInvoiceMutation.isSuccess && (
                        <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
                            <div className="flex items-center space-x-3">
                                <div className="rounded-full h-5 w-5 bg-green-600 flex items-center justify-center">
                                    <span className="text-white text-xs">
                                        ✓
                                    </span>
                                </div>
                                <span className="text-green-700 font-medium">
                                    Invoice parsed successfully!
                                </span>
                            </div>
                            <p className="text-green-600 text-sm mt-1">
                                Form fields have been automatically populated.
                                Please review and adjust as needed.
                            </p>
                        </div>
                    )}
                    {parseInvoiceMutation.isError && (
                        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                            <div className="flex items-center space-x-3">
                                <div className="rounded-full h-5 w-5 bg-red-600 flex items-center justify-center">
                                    <span className="text-white text-xs">
                                        !
                                    </span>
                                </div>
                                <span className="text-red-700 font-medium">
                                    Parsing failed
                                </span>
                            </div>
                            <p className="text-red-600 text-sm mt-1">
                                Unable to extract information from the document.
                                Please fill in the form manually.
                            </p>
                        </div>
                    )}
                    {!parseInvoiceMutation.isPending ? (
                        <AddInvoiceForm
                            parsedInvoice={parseInvoiceMutation.data}
                            clients={clients}
                            currencies={currencies}
                            file={file}
                        />
                    ) : (
                        <div className="flex flex-col items-center justify-center h-full py-10">
                            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-4"></div>
                            <span className="text-blue-700 font-medium text-lg">
                                Invoice is being parsed. Please wait...
                            </span>
                        </div>
                    )}
                </div>
            </div>
        </>
    );
}

export default AddInvoice;
