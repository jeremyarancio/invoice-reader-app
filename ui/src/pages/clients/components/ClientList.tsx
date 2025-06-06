import { Client } from "../types";
import TableRender from "@/common/components/TableRender";
import {
    useAddClient,
    useDeleteClients,
    useFetchClients,
    useUpdateClient,
} from "../hooks";
import { mapGetClientToClient } from "../mapper";
import { useState } from "react";
import AlertError from "@/common/components/AlertError";

const ClientList = () => {
    const pageNumber = 1;
    const perPage = 10;
    const [error, setError] = useState<Error | null>(null);
    const addClient = useAddClient();
    const updateClient = useUpdateClient();
    const fetchClients = useFetchClients();
    const deleteClients = useDeleteClients();

    const {
        data,
        isLoading,
        error: fetchError,
    } = fetchClients(pageNumber, perPage);

    const clients = data?.data.map(mapGetClientToClient) || [];

    if (isLoading) return <div>Loading clients...</div>;
    fetchError && setError(fetchError);

    const tableColumns = [
        { header: "Client", key: "name" },
        {
            header: "Total",
            key: "totalRevenu",
            render: (item: Client) => `$${item.totalRevenu}`,
        },
    ];

    const editFields = [
        { header: "Client Name", key: "name", formType: "text" as const },
        {
            header: "Street Number",
            key: "streetNumber",
            formType: "text" as const,
        },
        {
            header: "Street Address",
            key: "streetAddress",
            formType: "text" as const,
        },
        { header: "Zipcode", key: "zipcode", formType: "number" as const },
        { header: "City", key: "city", formType: "text" as const },
        { header: "Country", key: "country", formType: "text" as const },
    ];

    return (
        <>
            <div className="bg">
                {error && (
                    <AlertError error={error} onClose={() => setError(null)} />
                )}

                <div className="overflow-x-auto">
                    <div className="inline-block min-w-full align-middle">
                        <TableRender<Client>
                            name="Clients"
                            columns={tableColumns}
                            items={clients}
                            editFields={editFields}
                            onAddItem={addClient}
                            onUpdateItem={updateClient}
                            onDeleteItems={deleteClients}
                        />
                    </div>
                </div>
            </div>
        </>
    );
};

export default ClientList;
