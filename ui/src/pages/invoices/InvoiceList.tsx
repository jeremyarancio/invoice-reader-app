import { useState, useEffect } from "react";
import { Table, Alert, Button, Form, Dropdown } from "react-bootstrap";
import {
    fetchInvoices,
    deleteInvoices,
    updateInvoice,
} from "../../services/api";
import EditModal from "../../common/components/EditModal";
import { useMutation } from "@tanstack/react-query";
import { InvoiceRender, GetInvoicesResponse, Invoice } from "../../types";
import { useNavigate } from "react-router-dom";

const InvoiceList = () => {
    const [pageNumber, setPageNumber] = useState<number>(1);
    const [perPage, setPerPage] = useState<number>(10);
    const [invoiceRenderList, setInvoiceRenderList] = useState<InvoiceRender[]>(
        []
    );
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [totalInvoices, setTotalInvoices] = useState<number>(0);
    const [selectedInvoices, setSelectedInvoices] = useState<Invoice[]>([]);
    const [showedInvoice, setShowedInvoice] = useState<Invoice | null>(null);

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

    const handleDeleteSelected = (invoices: Invoice[]) => {
        if (invoices.length === 0) {
            alert("Please select invoices to delete");
            return;
        }

        if (window.confirm("Are you sure you want to delete this invoices?")) {
            const ids = invoices.map((invoice) => invoice.invoice_id);
            deleteInvoiceMutation.mutate(ids);
        }
    };

    const handleShow = (invoice: Invoice) => {
        console.log("AAA")
        setShowedInvoice(invoice);
    };

    const addInvoice = () => {
        navigate("/upload");
    };

    if (isLoading) return <div>Loading invoices...</div>;
    if (!sessionStorage.getItem("accessToken"))
        return (
            <Alert variant="danger">Log in to visualize your invoices...</Alert>
        );

    return (
        <>
            {showedInvoice && (
                <EditModal<Invoice>
                    entity={showedInvoice}
                    disabled={["invoice_id", "client_id"]}
                    onClose={() => setShowedInvoice(null)}
                    updateFn={updateInvoice}
                    deleteFn={() => deleteInvoices([showedInvoice.invoice_id])}
                />
            )}
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
                                    onClick={() => {
                                        handleDeleteSelected(selectedInvoices);
                                    }}
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
                            <tr key={item.data.invoice_number}>
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
                                <td>
                                    <img
                                        onClick={() => handleShow(item.data)}
                                        src="src/assets/eye-fill.svg"
                                        style={{ cursor: "pointer" }}
                                    ></img>
                                </td>
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
