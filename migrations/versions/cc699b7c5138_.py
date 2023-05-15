"""empty message

Revision ID: cc699b7c5138
Revises: 
Create Date: 2023-05-15 17:38:37.777193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc699b7c5138'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category_name', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sales_person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('sales_person', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_sales_person_username'), ['username'], unique=True)

    op.create_table('status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('status')
    )
    op.create_table('customer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('address', sa.String(length=512), nullable=True),
    sa.Column('salesperson_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['salesperson_id'], ['sales_person.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=512), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('warehouse_qty', sa.Integer(), nullable=True),
    sa.Column('active_qty', sa.Integer(), nullable=True),
    sa.Column('available_qty', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('img_src', sa.String(length=512), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status_id', sa.Integer(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['status.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('product_qty', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_details')
    op.drop_table('orders')
    op.drop_table('products')
    op.drop_table('customer')
    op.drop_table('status')
    with op.batch_alter_table('sales_person', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_sales_person_username'))

    op.drop_table('sales_person')
    op.drop_table('category')
    # ### end Alembic commands ###
