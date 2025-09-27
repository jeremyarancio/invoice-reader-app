import ClientCard from "@/components/ClientCard";
import NoElementFound from "@/components/NoElementFound";
import { Input } from "@/components/ui/input";
import { useFetchClients } from "@/hooks/api/client";
import { useNavigate } from "react-router-dom";

function Clients() {
    const navigate = useNavigate();
    const { clients, isLoading } = useFetchClients();

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
                <Input placeholder="Search"></Input>
            </div>
            {clients.length === 0 && !isLoading && (
                <NoElementFound type="client" />
            )}
            <div className="flex flex-col space-y-2 mt-5 mx-auto max-w-4xl px-4 h-full">
                {clients.map((client) => (
                    <ClientCard
                        key={client.clientName}
                        clientId={client.id}
                        clientName={client.clientName}
                        totalInvoice={client.nInvoices}
                        totalInvoiceAmount={client.totalRevenue}
                        totalInvoiceAmountCurrency={"-"}
                    />
                ))}
            </div>
        </>
    );
}

export default Clients;
