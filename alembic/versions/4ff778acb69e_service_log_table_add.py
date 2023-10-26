"""Service LOG Table Add
Revision ID: 4ff778acb69e
Revises: 
Create Date: 2023-10-25 08:04:51.264890
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4ff778acb69e'
down_revision = None
branch_labels = None
depends_on = None

# Upgrade DataBase
def upgrade() -> None:

    # Create Service LOG Table
    op.create_table('Service_LOG',
        
        # Columns
        sa.Column('Service_LOG_ID', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('Service', sa.String(), nullable=False),
        sa.Column('Service_Status', sa.Boolean, nullable=False),
        sa.Column('Service_Update_Time', sa.DateTime, nullable=False, server_default=sa.func.now())

    )

    # Pass
    pass

# Downgrade DataBase
def downgrade() -> None:

    # Drop Service LOG Table
    op.drop_table('Service_LOG')

    # Pass
    pass
