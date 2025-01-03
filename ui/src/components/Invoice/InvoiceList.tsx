import { useState, useEffect } from "react";
import { Table, Alert, Button, Form, Dropdown, Modal } from "react-bootstrap";
import {
    fetchInvoice,
    fetchInvoices,
    deleteInvoices,
    updateInvoice,
} from "../../services/api";
import { useMutation, useQuery } from "@tanstack/react-query";
import {
    InvoiceRender,
    GetInvoiceResponse,
    GetInvoicesResponse,
    Invoice,
} from "../../types";
import { useNavigate } from "react-router-dom";

const initialInvoice: Invoice = {
    amount_excluding_tax: 0,
    vat: 0,
    currency: "€",
    invoiced_date: new Date(),
    invoice_number: "",
    invoice_id: "",
    client_id: "",
};

const InvoiceList: React.FC = () => {
    const [pageNumber, setPageNumber] = useState<number>(1);
    const [perPage, setPerPage] = useState<number>(10);
    const [invoiceRenderList, setInvoiceRenderList] = useState<InvoiceRender[]>(
        []
    );
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [totalInvoices, setTotalInvoices] = useState<number>(0);
    const [selectedInvoices, setSelectedInvoices] = useState<Invoice[]>([]);
    const [show, setShow] = useState<boolean>(false);
    const [selectedInvoice, setSelectedInvoice] =
        useState<Invoice>(initialInvoice);
    const [showedInvoice, setShowedInvoice] = useState<Invoice>(initialInvoice);
    const [isFormDisabled, setIsFormDisabled] = useState<boolean>(true);
    const [editedInvoice, setEditedInvoice] = useState<Invoice>(initialInvoice);
    const [isEditToSubmit, setIsEditToSubmit] = useState<boolean>(false);

    const navigate = useNavigate();

    const InvoiceListMutation = useMutation({
        mutationFn: fetchInvoices,
        onSuccess: (response: GetInvoicesResponse) => {
            setError(null);
            const ExtractedInvoiceRender: InvoiceRender[] = response.data.map(
                (item) => ({
                    data: {
                        invoice_id: item.invoice_id,
                        invoice_number: item.data.invoice_number,
                        client_id: item.data.client_id,
                        currency: item.data.currency,
                        invoiced_date: item.data.invoiced_date,
                        amount_excluding_tax: item.data.amount_excluding_tax,
                        vat: item.data.vat,
                    },
                    clientName: item.data.client_id,
                    paid: true,
                })
            );

            setInvoiceRenderList(ExtractedInvoiceRender);
            setTotalInvoices(response.total);
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
            InvoiceListMutation.mutate({ pageNumber, perPage });
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

    const handleSelect = (invoice: Invoice) => {
        setSelectedInvoices((prevSelected) => {
            if (
                prevSelected.some(
                    (item) => item.invoice_id === invoice.invoice_id
                )
            ) {
                return prevSelected.filter(
                    (item) => item.invoice_id !== invoice.invoice_id
                );
            }
            return [...prevSelected, invoice];
        });
    };

    const handleSelectAll = () => {
        const allCurrentPageInvoices = invoiceRenderList.map(
            (item) => item.data
        );
        const areAllSelected = allCurrentPageInvoices.every((invoice) =>
            selectedInvoices.some(
                (selected) => selected.invoice_id === invoice.invoice_id
            )
        );

        if (areAllSelected) {
            setSelectedInvoices((prevSelected) =>
                prevSelected.filter(
                    (selected) =>
                        !allCurrentPageInvoices.some(
                            (invoice) =>
                                invoice.invoice_id === selected.invoice_id
                        )
                )
            );
        } else {
            setSelectedInvoices((prevSelected) => {
                const newSelected = [...prevSelected];
                allCurrentPageInvoices.forEach((invoice) => {
                    if (
                        !newSelected.some(
                            (selected) =>
                                selected.invoice_id === invoice.invoice_id
                        )
                    ) {
                        newSelected.push(invoice);
                    }
                });
                return newSelected;
            });
        }
    };

    const isInvoiceSelected = (invoice: Invoice) => {
        return selectedInvoices.some(
            (selected) => selected.invoice_id === invoice.invoice_id
        );
    };

    const areAllCurrentPageSelected = () => {
        return (
            invoiceRenderList.length > 0 &&
            invoiceRenderList.every((item) => isInvoiceSelected(item.data))
        );
    };

    const deleteInvoiceMutation = useMutation({
        mutationFn: deleteInvoices,
        onSuccess: () => {
            setSelectedInvoices([]);
            alert("Invoices deleted successfully");
        },
        onError: (error) => {
            alert("Failed to delete invoices: " + error.message);
        },
    });

    const handleDeleteSelected = () => {
        if (selectedInvoices.length === 0) {
            alert("Please select invoices to delete");
            return;
        }

        if (
            window.confirm(
                "Are you sure you want to delete the selected invoices?"
            )
        ) {
            const invoiceIds = selectedInvoices.map(
                (invoice) => invoice.invoice_id
            );
            deleteInvoiceMutation.mutate(invoiceIds);
        }
    };

    const handleClose = () => {
        setShow(false);
        setSelectedInvoice(initialInvoice);
        setShowedInvoice(initialInvoice);
        setIsEditToSubmit(false);
    };

    const handleShow = (invoice: Invoice) => {
        setShowedInvoice(invoice);
        setEditedInvoice(invoice); // In case of edition, we create a copy
        setShow(true);
    };

    const handleEdit = () => {
        setIsFormDisabled(false);
        setIsEditToSubmit(true);
    };

    const handleEditChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        if (!(name in editedInvoice)) {
            setError(`Invalid field name: ${name}`)
            console.error(error)
            return;
        }
        setEditedInvoice((prev) => ({
            ...prev,
            [name]: value,
        }));
        console.log(editedInvoice);
    };

    const updateInvoiceMutation = useMutation({
        mutationFn: updateInvoice,
        onSuccess: () => {
            setError(null);
            window.alert("Invoice successfully updated.");
            handleClose();
            // Need to update list of invoices with react-query
        },
        onError: (err) => {
            const errorMessage =
                err instanceof Error
                    ? err.message
                    : "An unexpected error occurred";
            setError(errorMessage);
            window.alert("Erreur: " + errorMessage);
        },
    });

    const handleSubmitEdition = (e: React.FormEvent) => {
        e.preventDefault();
        !error && updateInvoiceMutation.mutate(editedInvoice);
    };

    const addInvoice = () => {
        navigate("/upload");
    };

    if (isLoading) return <div>Loading invoices...</div>;
    // if (error)
    //     return (
    //         <Alert variant="danger">Log in to visualize your invoices...</Alert>
    //     );

    return (
        <>
            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Invoice</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form onSubmit={handleSubmitEdition}>
                        <Form.Group className="mb-3">
                            <Form.Label>Invoice number:</Form.Label>
                            <Form.Control
                                type="text"
                                autoFocus
                                name="invoice_number"
                                placeholder={showedInvoice?.invoice_number}
                                disabled={isFormDisabled}
                                onChange={handleEditChange}
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>Client name:</Form.Label>
                            <Form.Control type="text" autoFocus disabled />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>Amount excl. tax:</Form.Label>
                            <Form.Control
                                type="text"
                                autoFocus
                                name="amount_excluding_tax"
                                onChange={handleEditChange}
                                placeholder={showedInvoice?.amount_excluding_tax.toString()}
                                disabled={isFormDisabled}
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>VAT:</Form.Label>
                            <Form.Control
                                type="number"
                                autoFocus
                                name="vat"
                                onChange={handleEditChange}
                                placeholder={showedInvoice?.vat + "%"}
                                disabled={isFormDisabled}
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>Invoiced date</Form.Label>
                            <Form.Control
                                type="date"
                                autoFocus
                                name="invoiced_date"
                                onChange={handleEditChange}
                                value={showedInvoice?.invoiced_date.toString()}
                                disabled={isFormDisabled}
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>Last updated</Form.Label>
                            <Form.Control
                                type="text"
                                autoFocus
                                disabled // We keep this field disabled to let the BE takes charge of it
                            />
                        </Form.Group>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                        Close
                    </Button>
                    <Button variant="outline-danger">Delete</Button>
                    <Button
                        variant={isEditToSubmit ? "warning" : "primary"}
                        onClick={
                            isEditToSubmit ? handleSubmitEdition : handleEdit
                        }
                        type={isEditToSubmit ? "submit" : "button"}
                    >
                        {isEditToSubmit ? "Submit" : "Edit"}
                    </Button>
                </Modal.Footer>
            </Modal>
            <div>
                <h2>Invoices</h2>
                {selectedInvoices.length > 0 && (
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
                                    <img src="src/assets/trash.svg"></img>{" "}
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
                            <th>Invoice Number</th>
                            <th>Client id</th>
                            <th>Date</th>
                            <th>Amount (Excl. Tax)</th>
                            <th>VAT</th>
                        </tr>
                    </thead>
                    <tbody>
                        {invoiceRenderList.map((item) => (
                            <tr
                                key={item.data.invoice_number}
                                style={{ cursor: "pointer" }}
                                className="hover:bg-gray-50"
                                onClick={() => handleShow(item.data)}
                            >
                                <td>
                                    <Form.Check
                                        type="checkbox"
                                        className="mb-3"
                                        onChange={() => handleSelect(item.data)}
                                        checked={isInvoiceSelected(item.data)}
                                    />
                                </td>
                                <td>{item.data.invoice_number}</td>
                                <td>{item.clientName}</td>
                                <td>{item.data.invoiced_date?.toString()}</td>
                                <td>
                                    {item.data.currency}
                                    {item.data.amount_excluding_tax?.toFixed(0)}
                                </td>
                                <td>{item.data.vat}%</td>
                            </tr>
                        ))}
                    </tbody>
                </Table>
                <div className="text-muted">
                    Total Invoices: {totalInvoices}
                </div>
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
                                max={Math.ceil(totalInvoices / perPage)}
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
                    <Button onClick={addInvoice} variant="primary">
                        Add invoice
                    </Button>
                </div>
            </div>
        </>
    );
};

export default InvoiceList;
