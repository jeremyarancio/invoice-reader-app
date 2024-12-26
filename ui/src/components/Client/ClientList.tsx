import React, { useState, useEffect } from "react";
import { Table, Alert, Button, Dropdown, Form } from "react-bootstrap";
import { fetchClients, deleteClients } from "../../services/api";
import { useMutation } from "@tanstack/react-query";
import { Client, GetClientsResponse } from "../../types";
import ClientForm from "./ClientForm";

const ClientList: React.FC = () => {
    const [pageNumber, setPageNumber] = useState<number>(1);
    const [perPage, setPerPage] = useState<number>(10);
    const [clientList, setClientList] = useState<Client[]>([]);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [showForm, setShowForm] = useState<boolean>(false);
    const [selectedClients, setSelectedClients] = useState<Client[]>([]);

    const clientListMutation = useMutation({
        mutationFn: fetchClients,
        onSuccess: (response: GetClientsResponse) => {
            setError(null);

            setClientList(response.data);
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
            clientListMutation.mutate({ pageNumber, perPage });
        };
        fetchInvoices();
    }, [pageNumber, perPage]);

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

    const handleSelect = (client: Client) => {
        setSelectedClients((prevSelected) => {
            if (
                prevSelected.some((item) => item.client_id === client.client_id)
            ) {
                return prevSelected.filter(
                    (item) => item.client_id !== client.client_id
                );
            }
            return [...prevSelected, client];
        });
    };

    const handleSelectAll = () => {
        const areAllSelected = clientList.every((client) =>
            selectedClients.some(
                (selected) => selected.client_id === client.client_id
            )
        );
        if (areAllSelected) {
            setSelectedClients((prevSelected) =>
                prevSelected.filter(
                    (selected) =>
                        !clientList.some(
                            (client) => client.client_id === selected.client_id
                        )
                )
            );
        } else {
            setSelectedClients((prevSelected) => {
                const newSelected = [...prevSelected];
                clientList.forEach((client) => {
                    if (
                        !newSelected.some(
                            (selected) =>
                                selected.client_id === client.client_id
                        )
                    ) {
                        newSelected.push(client);
                    }
                });
                return newSelected;
            });
        }
    };

    const isClientSelected = (client: Client) => {
        return selectedClients.some(
            (selected) => selected.client_id === client.client_id
        );
    };

    const areAllCurrentPageSelected = () => {
        return (
            clientList.length > 0 &&
            clientList.every((item) => isClientSelected(item))
        );
    };

    const deleteInvoiceMutation = useMutation({
        mutationFn: deleteClients,
        onSuccess: () => {
            setSelectedClients([]);
            alert("Invoices deleted successfully");
            clientListMutation.mutate({ pageNumber, perPage });
        },
        onError: (error) => {
            alert("Failed to delete invoices: " + error.message);
        },
    });

    const handleDeleteSelected = () => {
        if (selectedClients.length === 0) {
            alert("Please select invoices to delete");
            return;
        }

        if (
            window.confirm(
                "Are you sure you want to delete the selected invoices?"
            )
        ) {
            const clientIds = selectedClients.map((client) => client.client_id);
            deleteInvoiceMutation.mutate(clientIds);
        }
    };


    if (isLoading) return <div>Loading invoices...</div>;
    if (showForm) return <ClientForm />;
    if (error)
        return (
            <Alert variant="danger">Log in to visualize your invoices...</Alert>
        );

    return (
        <div>
            <h2>Clients</h2>
            {selectedClients.length > 0 && (
                <div className="d-flex justify-content-end align-items-center">
                    <Dropdown>
                        <Dropdown.Toggle
                            variant="secondary"
                            id="dropdown-basic"
                        >
                            Actions
                        </Dropdown.Toggle>

                        <Dropdown.Menu>
                            <Dropdown.Item
                                href="#/delete"
                                onClick={handleDeleteSelected}
                            >
                                <img src="src/assets/trash.svg" alt="Delete" />{" "}
                                Delete
                            </Dropdown.Item>
                        </Dropdown.Menu>
                    </Dropdown>
                </div>
            )}
            <Table striped hover>
                <thead>
                    <tr>
                        <th>
                            <Form.Check
                                type="checkbox"
                                className="mb-1"
                                onChange={handleSelectAll}
                                checked={areAllCurrentPageSelected()}
                            />
                        </th>
                        <th>Client</th>
                        <th>Total revenue generated</th>
                    </tr>
                </thead>
                <tbody>
                    {clientList.map((item) => (
                        <tr key={item.client_id}>
                            <td>
                                <Form.Check
                                    type="checkbox"
                                    className="mb-3"
                                    onChange={() => handleSelect(item)}
                                    checked={isClientSelected(item)}
                                />
                            </td>
                            <td>{item.client_name}</td>
                            <td>{"1000€"}</td>
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
