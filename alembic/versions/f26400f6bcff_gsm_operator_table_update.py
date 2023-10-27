"""GSM Operator Table Update

Revision ID: f26400f6bcff
Revises: fafb5b003eda
Create Date: 2023-10-27 08:29:51.734495

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f26400f6bcff'
down_revision = 'fafb5b003eda'
branch_labels = None
depends_on = None

# Upgrade DataBase
def upgrade() -> None:

    # Drop MCC Table
    op.drop_table('GSM_MCC')

    # Drop MNC Table
    op.drop_table('GSM_MNC')

    # Create GSM_Operator Table
    op.create_table('GSM_Operator',
        sa.Column('Operator_ID', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('MCC_ID', sa.Integer, nullable=False),
        sa.Column('MCC_ISO', sa.String(), nullable=False),
        sa.Column('MCC_Country_Name', sa.String(), nullable=False),
        sa.Column('MCC_Country_Code', sa.Integer, nullable=True),
        sa.Column('MCC_Country_Flag_Image_URL', sa.String(), nullable=True),
        sa.Column('MNC_ID', sa.Integer, nullable=False),
        sa.Column('MNC_Brand_Name', sa.String(), nullable=False),
        sa.Column('MNC_Operator_Name', sa.String(), nullable=False),
        sa.Column('MNC_Operator_Image_URL', sa.String(), nullable=True)
    )

    # Drop SIM Table
    op.drop_table('SIM')

    # Create SIM Table
    op.create_table('SIM',
        sa.Column('SIM_ICCID', sa.String(), primary_key=True, nullable=False),
        sa.Column('Operator_ID', sa.Integer, nullable=False),
        sa.Column('SIM_GSM_Number', sa.String(), nullable=True),
        sa.Column('SIM_Static_IP', sa.String(), nullable=True),
        sa.Column('SIM_Create_Date', sa.DateTime, nullable=False, server_default=sa.func.now())
    )

    # Pass
    pass

# Downgrade DataBase
def downgrade() -> None:

    # Drop GSM_Operator Table
    op.drop_table('GSM_Operator')

    # Create MNC Table
    op.create_table('GSM_MNC',
        sa.Column('MNC_Record_ID', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('MCC_ID', sa.Integer, nullable=False),
        sa.Column('MNC_ID', sa.Integer, nullable=False),
        sa.Column('MNC_Brand_Name', sa.String(), nullable=False),
        sa.Column('MNC_Operator_Name', sa.String(), nullable=False),
        sa.Column('MNC_Operator_Image_URL', sa.String(), nullable=True)
    )

    # Create MCC Table
    op.create_table('GSM_MCC',
        sa.Column('MCC_ID', sa.Integer, primary_key=True, nullable=False),
        sa.Column('MCC_ISO', sa.String(), nullable=False),
        sa.Column('MCC_Country_Name', sa.String(), nullable=False),
        sa.Column('MCC_Country_Code', sa.Integer, nullable=False),
        sa.Column('MCC_Country_Flag_Image_URL', sa.String(), nullable=True)
    )

    # Drop SIM Table
    op.drop_table('SIM')

    # Create SIM Table
    op.create_table('SIM',
        sa.Column('SIM_ID', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('SIM_ICCID', sa.String(), nullable=False),
        sa.Column('MCC_ID', sa.Integer, nullable=False),
        sa.Column('MNC_ID', sa.Integer, nullable=False),
        sa.Column('SIM_Number', sa.String(), nullable=True),
        sa.Column('SIM_Static_IP', sa.String(), nullable=True),
        sa.Column('SIM_Status', sa.Boolean, nullable=False, server_default=sa.text('false')),
        sa.Column('SIM_Create_Date', sa.DateTime, nullable=False, server_default=sa.func.now())
    )

    # Pass
    pass
