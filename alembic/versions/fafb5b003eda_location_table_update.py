"""Location Table Update

Revision ID: fafb5b003eda
Revises: 92d535309acb
Create Date: 2023-10-26 13:45:28.098230

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'fafb5b003eda'
down_revision = '92d535309acb'
branch_labels = None
depends_on = None

# Upgrade DataBase
def upgrade() -> None:

    # Drop Location Table
    op.drop_table('Location')

    # Pass
    pass

# Downgrade DataBase
def downgrade() -> None:

    # Create Location Table
    op.create_table('Location',
        sa.Column('Location_ID', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('Device_ID', sa.String(), nullable=False),
        sa.Column('Location_TAC', sa.Integer, nullable=True),
        sa.Column('Location_LAC', sa.Integer, nullable=True),
        sa.Column('Location_Cell_ID', sa.Integer, nullable=True),
        sa.Column('Location_Latitude', sa.Float, nullable=True),
        sa.Column('Location_Longitude', sa.Float, nullable=True),
        sa.Column('Location_Date', sa.DateTime, nullable=False, server_default=sa.func.now())
    )

    # Pass
    pass
