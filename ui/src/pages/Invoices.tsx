import InvoiceCard from "@/components/InvoiceCard";
import NoElementFound from "@/components/NoElementFound";
import { Input } from "@/components/ui/input";
import UploadInvoiceModal from "@/components/UploadInvoiceModal";
import { useFetchCurrencies, useFetchInvoices } from "@/hooks/api/invoice";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Invoices() {
    const navigate = useNavigate();
    const [selectedFile, setSelectedFile] = useState(null);
    const fetchInvoices = useFetchInvoices();
    const fetchCurrencies = useFetchCurrencies();

    const { invoices } = fetchInvoices();
    const { currencies } = fetchCurrencies();

    const handleUpload = () => {
        selectedFile &&
            navigate("/invoices/add", {
                state: { file: selectedFile }, // Send file during navigation
            });
    };

    return (
        <>
            <div className="flex justify-around my-12">
                <h1>Invoices</h1>
                <UploadInvoiceModal
                    trigger={
                        <button className="button-primary">Add Invoice</button>
                    }
                    handleUpload={handleUpload}
                    setSelectedFile={setSelectedFile}
                />
            </div>

            <div className="max-w-96 px-4 mb-20 mx-auto mt-5">
                <Input placeholder="Search"></Input>
            </div>
            {invoices.length === 0 && <NoElementFound type="invoice" />}
            <div className="flex flex-col space-y-2 mt-5 mx-auto max-w-4xl px-4 h-full">
                {invoices?.map((invoice) => (
                    <InvoiceCard
                        key={invoice.invoiceNumber}
                        invoiceDescription={""} // Not implemented
                        grossAmount={invoice.grossAmount}
                        invoiceNumber={invoice.invoiceNumber}
                        issuedDate={invoice.issuedDate}
                        status={invoice.status ? "paid" : "unpaid"} //To change
                        currency={
                            currencies?.find((c) => c.id === invoice.currencyId)
                                ?.name ?? "-"
                        }
                    />
                ))}
            </div>
        </>
    );
}

export default Invoices;
