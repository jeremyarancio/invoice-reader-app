"""Database creation

Revision ID: 9ef3fa9f1cc8
Revises: 
Create Date: 2025-01-24 15:13:55.313973

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '9ef3fa9f1cc8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('is_disabled', sa.Boolean(), nullable=False),
    sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('client',
    sa.Column('client_id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('client_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('street_number', sa.Integer(), nullable=False),
    sa.Column('street_address', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('zipcode', sa.Integer(), nullable=False),
    sa.Column('city', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('country', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('client_id')
    )
    op.create_table('invoice',
    sa.Column('file_id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('client_id', sa.Uuid(), nullable=False),
    sa.Column('s3_path', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('invoice_number', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('amount_excluding_tax', sa.Float(), nullable=False),
    sa.Column('vat', sa.Float(), nullable=False),
    sa.Column('currency', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('is_paid', sa.Boolean(), nullable=False),
    sa.Column('invoiced_date', sa.Date(), nullable=False),
    sa.Column('uploaded_date', sa.Date(), nullable=True),
    sa.Column('last_updated_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['client.client_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('file_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('invoice')
    op.drop_table('client')
    op.drop_table('user')
    # ### end Alembic commands ###
