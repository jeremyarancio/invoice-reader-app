import { Alert } from "react-bootstrap";
import { Client } from "../types";
import TableRender from "@/common/components/TableRender";
import {
    useAddClient,
    useDeleteClients,
    useFetchClients,
    useUpdateClient,
} from "../hooks";
import { mapGetClientToClient } from "../mapper";

const ClientList = () => {
    const pageNumber = 1;
    const perPage = 10;
    const addClient = useAddClient();
    const updateClient = useUpdateClient();
    const fetchClients = useFetchClients();
    const deleteClients = useDeleteClients();

    const { data, isLoading, error } = fetchClients(pageNumber, perPage);
    const clients = data?.data.map(mapGetClientToClient) || [];

    if (isLoading) return <div>Loading clients...</div>;
    if (!localStorage.getItem("accessToken"))
        return <Alert variant="danger">You need to log in...</Alert>;

    const tableColumns = [
        { header: "Client", key: "name" },
        { header: "Total", key: "", render: () => `$${"..."}` },
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
            {error && <Alert variant="danger">Error:{error.message}</Alert>}
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
