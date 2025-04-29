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
        { header: "Client Name", key: "name" },
        { header: "Street Number", key: "streetNumber" },
        { header: "Street Address", key: "streetAddress" },
        { header: "Zipcode", key: "zipcode" },
        { header: "City", key: "city" },
        { header: "Country", key: "country" },
    ];

    return (
        <>
            {error && (
                <AlertError error={error} onClose={() => setError(null)} />
            )}
            <TableRender<Client>
                name="Clients"
                columns={tableColumns}
                items={clients}
                editFields={editFields}
                onAddItem={addClient}
                onUpdateItem={updateClient}
                onDeleteItems={deleteClients}
            />
        </>
    );
};

export default ClientList;
