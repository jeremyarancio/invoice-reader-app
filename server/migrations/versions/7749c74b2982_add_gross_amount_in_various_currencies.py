"""Add gross_amount in various currencies

Revision ID: 7749c74b2982
Revises: 143409f9beb3
Create Date: 2025-10-10 15:34:36.122129

"""
from typing import Sequence, Union
import json

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

from invoice_reader.infrastructure.exchange_rates import TestExchangeRatesService
from invoice_reader.domain.invoice import Currency


# revision identifiers, used by Alembic.
revision: str = '7749c74b2982'
down_revision: Union[str, None] = '143409f9beb3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add currency_amounts column and populate it with exchange rate data."""

    # Step 1: Add column as nullable
    op.add_column('invoice', sa.Column('currency_amounts', sa.JSON(), nullable=True))

    # Step 2: Populate data for existing rows
    connection = op.get_bind()

    # Fetch all invoices that need currency_amounts populated
    result = connection.execute(
        text("""
            SELECT invoice_id, gross_amount, currency, invoiced_date
            FROM invoice
            WHERE currency_amounts IS NULL
        """)
    )

    # Initialize exchange rate service (using test service for consistent rates)
    exchange_service = TestExchangeRatesService()

    rows = result.fetchall()
    total = len(rows)

    print(f"\nPopulating currency_amounts for {total} invoices...")

    for idx, row in enumerate(rows, 1):
        invoice_id = row[0]
        gross_amount = row[1]
        base_currency_str = row[2]
        issued_date = row[3]

        try:
            # Convert string to Currency enum
            base_currency = Currency(base_currency_str)

            # Fetch exchange rates for the invoice date
            exchange_rates = exchange_service.get_exchange_rates(
                base_currency=base_currency,
                date=issued_date
            )

            # Calculate currency amounts
            currency_amounts = {
                str(cur): float(rate * gross_amount)
                for cur, rate in exchange_rates.items()
            }

            print(f"  [{idx}/{total}] Invoice {invoice_id}: {base_currency} {gross_amount} -> {len(currency_amounts)} currencies")

        except Exception as e:
            # Fallback: just store base currency if something fails
            print(f"  [{idx}/{total}] WARNING: Failed to fetch rates for invoice {invoice_id}: {e}")
            print(f"            Falling back to base currency only")
            currency_amounts = {base_currency_str: float(gross_amount)}

        # Update the row
        connection.execute(
            text("""
                UPDATE invoice
                SET currency_amounts = :amounts
                WHERE invoice_id = :id
            """),
            {"amounts": json.dumps(currency_amounts), "id": str(invoice_id)}
        )

    print(f"✓ Successfully populated {total} invoices\n")

    # Step 3: Make column non-nullable
    op.alter_column('invoice', 'currency_amounts', nullable=False)


def downgrade() -> None:
    """Remove currency_amounts column."""
    op.drop_column('invoice', 'currency_amounts')
