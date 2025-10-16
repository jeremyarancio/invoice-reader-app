import { useFetchClient } from "@/hooks/api/client";
import { useNavigate, useParams } from "react-router-dom";
import ViewClientForm from "@/components/ViewClientForm";
import { ArrowLeft } from "lucide-react";
import { useCurrencyStore } from "@/stores/currencyStore";

function ViewClient() {
    const { clientId } = useParams();
    const navigate = useNavigate();
    const { client, isLoading: isClientLoading } = useFetchClient(clientId);
    const { selectedCurrency } = useCurrencyStore();

    return (
        <>
            <div className="mt-10 ml-10">
                <button
                    onClick={() => navigate("/clients")}
                    className="hover:cursor-pointer"
                >
                    <ArrowLeft
                        size={40}
                        className="rounded-full hover:bg-stone-50"
                    />
                </button>
            </div>
            <div className="flex flex-col mt-10 mb-40 px-4 md:px-20 max-w-4xl mx-auto">
                <h1 className="text-2xl font-bold">Client Details</h1>
                <div className="bg-card p-6 rounded-lg border shadow-sm mt-6">
                    {!isClientLoading && client && (
                        <ViewClientForm client={client} />
                    )}
                </div>
                <div className="bg-card p-6 rounded-lg border shadow-sm mt-6">
                    <h2 className="text-xl font-semibold mb-4">
                        Revenue Information
                    </h2>
                    <div className="flex justify-between items-center">
                        <span className="text-muted-foreground">
                            Total Revenue ({selectedCurrency}):
                        </span>
                        <div className="font-semibold text-lg">
                            {client?.totalRevenue?.[selectedCurrency]?.toFixed(2) || '0.00'} {selectedCurrency}
                        </div>
                    </div>
                </div>

                <div className="bg-card p-6 rounded-lg border shadow-sm mt-6">
                    <h2 className="text-xl font-semibold mb-4">
                        Client Invoices
                    </h2>
                    <p className="text-muted-foreground">
                        No invoices found for this client.
                    </p>
                </div>
            </div>
        </>
    );
}

export default ViewClient;
