import React, { useState, useEffect } from "react";
import { Table, Alert, Button } from "react-bootstrap";
import { getAllInvoice } from "../../services/api";
import { useMutation } from "@tanstack/react-query";
import { InvoiceDataRender, GetInvoicesResponse } from "../../types";
import { useNavigate } from "react-router-dom";

const InvoiceList: React.FC = () => {
    const [pageNumber, setPageNumber] = useState<number>(1);
    const [perPage, setPerPage] = useState<number>(10);
    const [invoiceRenderList, setInvoiceRenderList] = useState<
        InvoiceDataRender[]
    >([]);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [totalInvoices, setTotalInvoices] = useState<number>(0);
    const navigate = useNavigate();

    const InvoiceListMutation = useMutation({
        mutationFn: getAllInvoice,
        onSuccess: (response: GetInvoicesResponse) => {
            setError(null);

            const ExtractedInvoiceRender: InvoiceDataRender[] =
                response.data.map((item) => ({
                    invoiceNumber: item.data.invoice_number,
                    clientName: item.data.client_name,
                    invoicedDate: item.data.invoiced_date,
                    amountExcludingTax: item.data.amount_excluding_tax,
                    vat: item.data.vat,
                    currency: item.data.currency,
                }));

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

    const addInvoice = () => {
        navigate("/upload");
    };

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
                        <th>Invoice Number</th>
                        <th>Client Name</th>
                        <th>Date</th>
                        <th>Amount (Excl. Tax)</th>
                        <th>VAT</th>
                    </tr>
                </thead>
                <tbody>
                    {invoiceRenderList.map((item) => (
                        <tr key={item.invoiceNumber}>
                            <td>{item.invoiceNumber}</td>
                            <td>{item.clientName}</td>
                            <td>{item.invoicedDate.toString()}</td>
                            <td>
                                {item.currency}
                                {item.amountExcludingTax.toFixed(0)}
                            </td>
                            <td>{item.vat}%</td>
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
