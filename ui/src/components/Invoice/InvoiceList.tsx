import { useState } from "react";
import { InvoiceDataRender } from "../../types";
import { Table } from "react-bootstrap";

const InvoiceList = () => {
    const [invoices, setInvoices] = useState<InvoiceDataRender[]>([
        {
            id: 1,
            number: "INV001",
            clientName: "Client A",
            date: "2023-12-01",
            revenue: 1000,
            paid: true,
        },
        {
            id: 2,
            number: "INV002",
            clientName: "Client B",
            date: "2023-11-20",
            revenue: 1500,
            paid: false,
        },
    ]);

    return (
        <div>
            <h2>Invoices</h2>
            <Table striped hover onClick={() => console.log("clicked")}>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Invoice Number</th>
                        <th>Client Name</th>
                        <th>Date</th>
                        <th>Revenue</th>
                        <th>Paid</th>
                    </tr>
                </thead>
                <tbody>
                    {invoices.map((invoice) => (
                        <tr key={invoice.id}>
                            <td>{invoice.id}</td>
                            <td>{invoice.number}</td>
                            <td>{invoice.clientName}</td>
                            <td>{invoice.date}</td>
                            <td>${invoice.revenue.toFixed(2)}</td>
                            <td>{invoice.paid ? "Yes" : "No"}</td>
                        </tr>
                    ))}
                </tbody>
            </Table>
        </div>
    );
};

export default InvoiceList;
