"""Measurement Tables Update

Revision ID: 92d535309acb
Revises: 4ff778acb69e
Create Date: 2023-10-25 09:21:52.735213

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '92d535309acb'
down_revision = '4ff778acb69e'
branch_labels = None
depends_on = None

# Upgrade DataBase
def upgrade() -> None:
    
    # Drop Measurement Table
    op.drop_table('Measurement')

    # Create Measurement_Device Table
    op.create_table('Measurement_Device',
        sa.Column('Measurement_ID', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('Data_Stream_ID', sa.Integer, nullable=False),
        sa.Column('Device_ID', sa.String(), nullable=False),
        sa.Column('Measurement_Type_ID', sa.Integer, nullable=False),
        sa.Column('Measurement_Data_Count', sa.Integer, nullable=False),
        sa.Column('Measurement_Value', sa.Float, nullable=False),
        sa.Column('Measurement_Create_Date', sa.DateTime, nullable=False, server_default=sa.func.now())
    )

    # Create Measurement_WeatherStat Table
    op.create_table('Measurement_WeatherStat',
        sa.Column('Measurement_ID', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('Data_Stream_ID', sa.Integer, nullable=False),
        sa.Column('Device_ID', sa.String(), nullable=False),
        sa.Column('Measurement_Type_ID', sa.Integer, nullable=False),
        sa.Column('Measurement_Data_Count', sa.Integer, nullable=False),
        sa.Column('Measurement_Value', sa.Float, nullable=False),
        sa.Column('Measurement_State', sa.Boolean, nullable=True),
        sa.Column('Measurement_Min', sa.Float, nullable=True),
        sa.Column('Measurement_Max', sa.Float, nullable=True),
        sa.Column('Measurement_Avg', sa.Float, nullable=True),
        sa.Column('Measurement_Q1', sa.Float, nullable=True),
        sa.Column('Measurement_Q2', sa.Float, nullable=True),
        sa.Column('Measurement_Q3', sa.Float, nullable=True),
        sa.Column('Measurement_Deviation', sa.Float, nullable=True),
        sa.Column('Measurement_Create_Date', sa.DateTime, nullable=False, server_default=sa.func.now())
    )
    
    # Pass
    pass

# Downgrade DataBase
def downgrade() -> None:

    # Drop Measurement_WeatherStat Table
    op.drop_table('Measurement_WeatherStat')

    # Drop Measurement_Device Table
    op.drop_table('Measurement_Device')

    # Create Measurement Table
    op.create_table('Measurement',
        sa.Column('Measurement_ID', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('Data_Stream_ID', sa.Integer, nullable=False),
        sa.Column('Device_ID', sa.String(), nullable=False),
        sa.Column('Measurement_Type_ID', sa.Integer, nullable=False),
        sa.Column('Measurement_Data_Count', sa.Integer, nullable=False),
        sa.Column('Measurement_Value', sa.Float, nullable=False),
        sa.Column('Measurement_State', sa.Boolean, nullable=True),
        sa.Column('Measurement_Min', sa.Float, nullable=True),
        sa.Column('Measurement_Max', sa.Float, nullable=True),
        sa.Column('Measurement_Avg', sa.Float, nullable=True),
        sa.Column('Measurement_Q1', sa.Float, nullable=True),
        sa.Column('Measurement_Q2', sa.Float, nullable=True),
        sa.Column('Measurement_Q3', sa.Float, nullable=True),
        sa.Column('Measurement_Deviation', sa.Float, nullable=True),
        sa.Column('Measurement_Create_Date', sa.DateTime, nullable=False, server_default=sa.func.now())
    )

    # Pass
    pass
