"""Add currencies

Revision ID: 52a7478747a7
Revises: 9ef3fa9f1cc8
Create Date: 2025-03-13 15:57:45.285540

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

from invoice_reader.models import CurrencyModel, InvoiceModel

# revision identifiers, used by Alembic.
revision: str = "52a7478747a7"
down_revision: Union[str, None] = "9ef3fa9f1cc8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()
    session = sqlmodel.Session(bind=bind)

    op.create_table(
        "currency",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("currency", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    currency_dollar_id = session.exec(
        sqlmodel.select(CurrencyModel).where(CurrencyModel.currency == "$")
    ).one()

    op.add_column(
        "invoice",
        sa.Column(
            "currency_id", sa.Uuid(), nullable=True, default=str(currency_dollar_id.id)
        ),
    )
    op.drop_column("invoice", "currency")
    op.create_foreign_key(None, "invoice", "currency", ["currency_id"], ["id"])

    currencies = [
        CurrencyModel(currency="$"),
        CurrencyModel(currency="€"),
    ]
    session.add_all(currencies)
    session.commit()
    # ### end Alembic commands ###


def downgrade() -> None:
    """Big issue here: cannot downgrade because currency already exists as relationship.
    Do it manually or replace currency_column_name. Should be ok if no downgrade at this step.
    """
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "invoice",
        sa.Column("currency", sa.VARCHAR(), autoincrement=False),
    )

    session = sqlmodel.Session(bind=op.get_bind())
    invoice_models = session.exec(sqlmodel.select(InvoiceModel)).all()

    currency_euro_id = session.exec(
        sqlmodel.select(CurrencyModel).where(CurrencyModel.currency == "€")
    ).one()

    for invoice_model in invoice_models:
        invoice_model.currency = (
            "€" if invoice_model.currency_id == currency_euro_id.id else "$"
        )
    session.add_all(invoice_models)
    session.commit()

    op.drop_constraint(None, "invoice", type_="foreignkey")
    op.drop_column("invoice", "currency_id")
    op.drop_table("currency")
    # ### end Alembic commands ###
