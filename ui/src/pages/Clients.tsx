import ClientCard from "@/components/ClientCard";
import NoElementFound from "@/components/NoElementFound";
import { Input } from "@/components/ui/input";
import { useFetchClients } from "@/hooks/api/client";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Clients() {
    const navigate = useNavigate();
    const [searchQuery, setSearchQuery] = useState("");

    const { clients, isLoading } = useFetchClients();

    const filteredClients = clients?.filter((client) => {
        const query = searchQuery.toLowerCase();

        return (
            client.clientName.toLowerCase().includes(query) ||
            client.city.toLowerCase().includes(query) ||
            client.country.toLowerCase().includes(query) ||
            client.streetAddress.toLowerCase().includes(query)
        );
    });

    return (
        <>
            <div className="flex justify-around my-12">
                <h1>Clients</h1>
                <button
                    onClick={() => navigate("/clients/add")}
                    className="button-primary"
                >
                    Add Client
                </button>
            </div>
            <div className="max-w-96 px-4 mb-20 mx-auto mt-5">
                <Input
                    placeholder="Search clients..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
            </div>
            {filteredClients.length === 0 && !isLoading && (
                <NoElementFound type="client" />
            )}
            <div className="flex flex-col space-y-2 mt-5 mx-auto max-w-4xl px-4 h-full">
                {filteredClients?.map((client) => (
                    <div
                        key={client.id}
                        className="animate-in fade-in slide-in-from-top-2 duration-300"
                    >
                        <ClientCard
                            clientId={client.id}
                            clientName={client.clientName}
                            totalInvoice={client.nInvoices}
                            totalInvoiceAmount={client.totalRevenue}
                            totalInvoiceAmountCurrency={"-"}
                        />
                    </div>
                ))}
            </div>
        </>
    );
}

export default Clients;
