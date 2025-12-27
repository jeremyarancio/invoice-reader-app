import { useFetchClient, useFetchClientRevenue } from "@/hooks/api/client";
import { useNavigate, useParams } from "react-router-dom";
import ViewClientForm from "@/components/ViewClientForm";
import { ArrowLeft } from "lucide-react";
import { useCurrencyStore } from "@/stores/currencyStore";
import { Skeleton } from "@/components/ui/skeleton";
import { CURRENCIES } from "@/schemas/invoice";

function ViewClient() {
    const { clientId } = useParams();
    const navigate = useNavigate();
    const { client, isLoading: isClientLoading } = useFetchClient(clientId!);
    const { clientRevenue, isLoading: isClientRevenueLoading } =
        useFetchClientRevenue(clientId!);
    const { selectedCurrency } = useCurrencyStore();

    const isLoading = isClientLoading || isClientRevenueLoading;

    if (isLoading) {
        return (
            <>
                <div className="mt-10 ml-10 mb-20">
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
                <div className="flex flex-col items-center mx-auto max-w-lg space-y-8">
                    {[
                        Array.from({ length: 2 }, (_, index) => (
                            <div
                                key={index}
                                className="bg-card p-6 rounded-lg border shadow-sm w-full "
                            >
                                <Skeleton className="h-10 w-1/3 mb-2 bg-foreground opacity-10" />
                                <Skeleton className="h-10 w-2/3 mb-2 bg-foreground opacity-10" />
                                <Skeleton className="h-10 w-full mb-2 bg-foreground opacity-10" />
                            </div>
                        )),
                    ]}
                </div>
            </>
        );
    }

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
                    {client && <ViewClientForm client={client} />}
                </div>
                <div className="bg-card p-6 rounded-lg border shadow-sm mt-6">
                    <h2 className="text-xl font-semibold mb-4">
                        Revenue Information
                    </h2>
                    <div className="flex justify-between items-center">
                        <span className="text-muted-foreground">
                            Estimated total Revenue ({selectedCurrency}):
                        </span>
                        <div className="font-semibold text-lg">
                            {clientRevenue?.total_revenue
                                ? `${
                                      clientRevenue.total_revenue[
                                          selectedCurrency
                                      ]?.toFixed(1) || "0.0"
                                  } ${CURRENCIES[selectedCurrency].symbol}`
                                : "Unable to calculate."}
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
