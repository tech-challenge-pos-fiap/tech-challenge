"""add_mercado_pago_fields_to_payment_table

Revision ID: a74453ed5e52
Revises: d67c5d6696d1
Create Date: 2025-08-03 18:34:50.462022

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a74453ed5e52'
down_revision: Union[str, None] = 'd67c5d6696d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add Mercado Pago fields to payments table
    op.add_column('payments', sa.Column('mp_payment_id', sa.String(255), nullable=True))
    op.add_column('payments', sa.Column('mp_status', sa.String(50), nullable=True))
    op.add_column('payments', sa.Column('mp_status_detail', sa.String(255), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove Mercado Pago fields from payments table
    op.drop_column('payments', 'mp_status_detail')
    op.drop_column('payments', 'mp_status')
    op.drop_column('payments', 'mp_payment_id')
