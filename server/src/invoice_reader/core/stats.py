from invoice_reader.models import ClientModel


def compute_total_revenu_per_client(client: ClientModel) -> float:
    return sum([invoice.amount_excluding_tax for invoice in client.invoices])
