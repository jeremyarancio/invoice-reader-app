import React, { useState, useEffect } from "react";
import { Table, Alert, Button } from "react-bootstrap";
import { fetchClients } from "../../services/api";
import { useMutation } from "@tanstack/react-query";
import { ClientDataRender, GetClientsResponse } from "../../types";
import ClientForm from "./ClientForm";

const ClientList: React.FC = () => {
    const [pageNumber, setPageNumber] = useState<number>(1);
    const [perPage, setPerPage] = useState<number>(10);
    const [ClientRenderList, setClientList] = useState<ClientDataRender[]>([]);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [showForm, setShowForm] = useState<boolean>(false);

    const ClientListMutation = useMutation({
        mutationFn: fetchClients,
        onSuccess: (response: GetClientsResponse) => {
            setError(null);

            const ExtractedClientRender: ClientDataRender[] = response.data.map(
                (item) => ({
                    name: item.client_name,
                    total: 1000, //Total revenu per client
                })
            );

            setClientList(ExtractedClientRender);
            setIsLoading(false);
        },
        onError: (error: Error) => {
            setError(error.message || "Failed to load invoices.");
            console.error(error);
            setIsLoading(false);
        },
    });

    useEffect(() => {
        const fetchInvoices = () => {
            setIsLoading(true);
            setError(null);
            ClientListMutation.mutate({ pageNumber, perPage });
        };

        fetchInvoices();
    }, [pageNumber, perPage]);

    if (isLoading) return <div>Loading invoices...</div>;
    if (showForm) return <ClientForm />;
    if (error)
        return (
            <Alert variant="danger">Log in to visualize your invoices...</Alert>
        );

    const handlePageChange = (newPage: number) => {
        setPageNumber(newPage);
    };

    const handlePerPageChange = (newPerPage: number) => {
        setPerPage(newPerPage);
        setPageNumber(1);
    };

    const addClient = () => {
        setShowForm(true);
    };

    return (
        <div>
            <h2>Clients</h2>
            <Table striped hover>
                <thead>
                    <tr>
                        <th>Client</th>
                        <th>Total revenu generated</th>
                    </tr>
                </thead>
                <tbody>
                    {ClientRenderList.map((item) => (
                        <tr key={item.name}>
                            <td>{item.name}</td>
                            <td>{item.total}€</td>
                        </tr>
                    ))}
                </tbody>
            </Table>
            <div className="mb-3 d-flex justify-content-end align-items-center">
                <div className="me-3">
                    <label className="me-2">
                        Page:
                        <input
                            type="number"
                            value={pageNumber}
                            onChange={(e) =>
                                handlePageChange(Number(e.target.value))
                            }
                            min="1"
                            className="form-control d-inline-block w-auto ms-2"
                        />
                    </label>
                </div>
                <div>
                    <label>
                        Per Page:
                        <select
                            value={perPage}
                            onChange={(e) =>
                                handlePerPageChange(Number(e.target.value))
                            }
                            className="form-control d-inline-block w-auto ms-2"
                        >
                            <option value={10}>10</option>
                            <option value={25}>25</option>
                            <option value={50}>50</option>
                        </select>
                    </label>
                </div>
            </div>
            <div className="mb-3 d-flex justify-content-end align-items-center">
                <Button onClick={addClient} variant="primary">
                    New client
                </Button>
            </div>
        </div>
    );
};

export default ClientList;
