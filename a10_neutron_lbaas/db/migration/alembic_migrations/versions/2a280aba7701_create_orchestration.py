"""create orchestration

Revision ID: 2a280aba7701
Revises: 579f359e6e30
Create Date: 2016-04-12 18:25:17.910876

"""

# revision identifiers, used by Alembic.
revision = '2a280aba7701'
down_revision = '579f359e6e30'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'a10_device_instances',
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('tenant_id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(1024), nullable=False),
        sa.Column('username', sa.String(255), nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('nova_instance_id', sa.String(36), nullable=False),
        sa.Column('ip_address', sa.String(255))
    )
    op.create_table(
        'a10_slbs',
        sa.Column('id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('tenant_id', sa.String(36), nullable=False),
        sa.Column('device_name', sa.String(1024), nullable=False),
        sa.Column('vip_id', sa.String(36)),
        sa.Column('loadbalancer_id', sa.String(36)),
    )
    pass


def downgrade():
    op.drop_table('a10_slbs')
    op.drop_table('a10_device_instances')
    pass