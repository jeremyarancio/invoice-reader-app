export interface ParsedInvoice {
    invoice: {
        gross_amount: number;
        vat: number;
        issued_date: string;
        invoice_number: string;
        invoice_description: string;
        currency_id: string;
    };
    client: {
        client_id: string;
        address: {
            street_address: string;
            zipcode: string;
            city: string;
            country: string;
        };
    };
    seller: {
        name: string;
        address: {
            street_address: string;
            zipcode: string;
            city: string;
            country: string;
        };
    };
}
