"""add_indexes_for_performance_optimization

Revision ID: b9132a7f4e12
Revises: a74453ed5e52
Create Date: 2025-10-05 17:42:00.000000

"""
from typing import Sequence, Union
from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'b9132a7f4e12'
down_revision: Union[str, None] = 'a74453ed5e52'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index(
        'idx_customer_email_unique',
        'customers',
        ['email'],
        unique=True
    )

    op.create_index(
        'idx_order_customer_id',
        'orders',
        ['customer_id']
    )

    op.create_index(
        'idx_order_items_order_id',
        'order_items',
        ['order_id']
    )
    op.create_index(
        'idx_order_items_product_id',
        'order_items',
        ['product_id']
    )

    op.create_index(
        'idx_payment_order_id',
        'payments',
        ['order_id']
    )

    op.create_index(
        'idx_product_name',
        'products',
        ['name']
    )
    op.create_index(
        'idx_product_category',
        'products',
        ['category']
    )

    op.create_index(
        'idx_order_items_order_product',
        'order_items',
        ['order_id', 'product_id']
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index('idx_order_items_order_product', table_name='order_items')
    op.drop_index('idx_product_category', table_name='products')
    op.drop_index('idx_product_name', table_name='products')
    op.drop_index('idx_payment_order_id', table_name='payments')
    op.drop_index('idx_order_items_product_id', table_name='order_items')
    op.drop_index('idx_order_items_order_id', table_name='order_items')
    op.drop_index('idx_order_customer_id', table_name='orders')
    op.drop_index('idx_customer_email_unique', table_name='customers')
