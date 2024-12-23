import React, { useState, useEffect } from "react";
import { Table, Alert, Button, Form, Modal } from "react-bootstrap";
import { getAllInvoice } from "../../services/api";
import { useMutation } from "@tanstack/react-query";
import { InvoiceRender, GetInvoicesResponse, Invoice } from "../../types";
import { useNavigate } from "react-router-dom";

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
    const navigate = useNavigate();

    const InvoiceListMutation = useMutation({
        mutationFn: getAllInvoice,
        onSuccess: (response: GetInvoicesResponse) => {
            setError(null);
            console.log(response);
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
        setSelectedInvoices(prevSelected => {
            if (prevSelected.includes(invoice)) {
                return prevSelected.filter(item => item.invoice_id !== invoice.invoice_id);
            }
            return [...prevSelected, invoice];
        });
    };

    const handleSelectAll = () => {
        if (selectedInvoices.length === invoiceRenderList.length) {
            setSelectedInvoices([]);
        } else {
            setSelectedInvoices(invoiceRenderList.map(item => item.data));
        }
    };

    const addInvoice = () => {
        navigate("/upload");
    };

    console.log(selectedInvoices)
    if (isLoading) return <div>Loading invoices...</div>;
    if (error)
        return (
            <Alert variant="danger">Log in to visualize your invoices...</Alert>
        );

    return (
        <div>
            <h2>Invoices</h2>
            <Table striped hover>
                <thead>
                    <tr>
                        <th>
                            <Form.Check
                                type="checkbox"
                                className="mb-1"
                                onChange={() => handleSelectAll()}
                            ></Form.Check>
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
                                    checked={selectedInvoices.length === invoiceRenderList.length}
                                ></Form.Check>
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
            <div className="text-muted">Total Invoices: {totalInvoices}</div>
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
    );
};

export default InvoiceList;
