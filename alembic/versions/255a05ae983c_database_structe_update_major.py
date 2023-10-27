"""Database Structe Update (Major)

Revision ID: 255a05ae983c
Revises: f26400f6bcff
Create Date: 2023-10-27 15:27:18.616602

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = '255a05ae983c'
down_revision = 'f26400f6bcff'
branch_labels = None
depends_on = None

# Upgrade DataBase
def upgrade() -> None:
    
    # Drop All Tables
    op.drop_table('Connection')
    op.drop_table('Data_Stream')
    op.drop_table('Device')
    op.drop_table('GSM_Operator')
    op.drop_table('IoT_Module')
    op.drop_table('Measurement_Device')
    op.drop_table('Measurement_Type')
    op.drop_table('Measurement_WeatherStat')
    op.drop_table('Module_Manufacturer')
    op.drop_table('Module_Model')
    op.drop_table('Module_Type')
    op.drop_table('RAW_Data')
    op.drop_table('Register')
    op.drop_table('Service_LOG')
    op.drop_table('Settings')
    op.drop_table('SIM')
    op.drop_table('Version')

    # Create Operator Table
    op.create_table('Operator',
        sa.Column('Operator_ID', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('MCC_ID', sa.Integer, nullable=False, default=0),
        sa.Column('MCC_ISO', sa.String(3), nullable=False, default=""),
        sa.Column('MCC_Country_Name', sa.String(50), nullable=False, default=""),
        sa.Column('MCC_Country_Code', sa.Integer, nullable=True, default=None),
        sa.Column('MCC_Country_Flag_Image_URL', sa.String(255), nullable=True, default=None),
        sa.Column('MNC_ID', sa.Integer, nullable=False, default=0),
        sa.Column('MNC_Brand_Name', sa.String(50), nullable=False, default=""),
        sa.Column('MNC_Operator_Name', sa.String(50), nullable=False, default=""),
        sa.Column('MNC_Operator_Image_URL', sa.String(255), nullable=True, default=None)
    )

    # SIM table
    op.create_table('SIM',
        sa.Column('ICCID', sa.String(20), primary_key=True, nullable=False),
        sa.Column('Operator_ID', sa.Integer, sa.ForeignKey('Operator.Operator_ID'), nullable=False, default=0),
        sa.Column('GSM_Number', sa.String(15), nullable=True, default=None),
        sa.Column('Static_IP', sa.String(15), nullable=True, default=None),
        sa.Column('Create_Time', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    )    

    # Manufacturer table
    op.create_table('Manufacturer',
        sa.Column('Manufacturer_ID', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('Manufacturer', sa.String(50), nullable=False, default="")
    )

    # Model table
    op.create_table('Model',
        sa.Column('Model_ID', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('Model', sa.String(50), nullable=False, default="")
    )

    # Modem table
    op.create_table('Modem',
        sa.Column('IMEI', sa.String(20), primary_key=True, nullable=False),
        sa.Column('Manufacturer_ID', sa.Integer, sa.ForeignKey('Manufacturer.Manufacturer_ID'), nullable=False, default=0),
        sa.Column('Model_ID', sa.Integer, sa.ForeignKey('Model.Model_ID'), nullable=False, default=0),
        sa.Column('Firmware', sa.String(10), nullable=True, default=None),
        sa.Column('Create_Time', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    )

    # Stream table
    op.create_table('Stream',
        sa.Column('Stream_ID', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('Device_ID', sa.String(50), sa.ForeignKey('Device.Device_ID'), nullable=False, default=""),
        sa.Column('IMEI', sa.String(20), sa.ForeignKey('Modem.IMEI'), nullable=False, default=""),
        sa.Column('ICCID', sa.String(20), sa.ForeignKey('SIM.ICCID'), nullable=False, default=""),
        sa.Column('RSSI', sa.Integer, nullable=True, default=None),
        sa.Column('TAC', sa.Integer, nullable=True, default=None),
        sa.Column('LAC', sa.Integer, nullable=True, default=None),
        sa.Column('Cell_ID', sa.Integer, nullable=True, default=None),
        sa.Column('Device_IP', sa.String, nullable=True, default=None),
        sa.Column('Connection_Time', sa.Integer, nullable=True, default=None),
        sa.Column('Size', sa.Integer, nullable=True, default=None),
        sa.Column('Create_Time', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    )

    # Version table
    op.create_table('Version',
        sa.Column('Version_ID', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('Device_ID', sa.String(50), nullable=False, default=""),
        sa.Column('Firmware', sa.String(10), nullable=True, default=None),
        sa.Column('Hardware', sa.String(10), nullable=True, default=None),
        sa.Column('Update_Time', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    )

    # Device table
    op.create_table('Device',
        sa.Column('Device_ID', sa.String(50), primary_key=True, nullable=False),
        sa.Column('Version_ID', sa.Integer, sa.ForeignKey('Version.Version_ID'), nullable=False, default=0),
        sa.Column('Model_ID', sa.Integer, nullable=False, default=0),
        sa.Column('Status', sa.Boolean, nullable=False, default=False, server_default=text('false')),
        sa.Column('Create_Date', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    )

    # Measurement_Type table
    op.create_table('Measurement_Type',
        sa.Column('Type_ID', sa.Integer, primary_key=True, nullable=False),
        sa.Column('Description', sa.String(255), nullable=False, default=""),
        sa.Column('Variable', sa.String(10), nullable=True, default=None),
        sa.Column('Unit', sa.String(10), nullable=True, default=None),
        sa.Column('Segment', sa.Integer, nullable=False, default=0)
    )

    # Parameter table
    op.create_table('Parameter',
        sa.Column('Parameter_ID', sa.Integer, primary_key=True, nullable=False),
        sa.Column('Stream_ID', sa.Integer, sa.ForeignKey('Stream.Stream_ID'), nullable=False, default=0),
        sa.Column('Type_ID', sa.Integer, sa.ForeignKey('Measurement_Type.Type_ID'), nullable=False, default=0),
        sa.Column('Value', sa.Float, nullable=True, default=None),
        sa.Column('Create_Time', sa.TIMESTAMP(timezone=True), nullable=False)
    )

    # Measurement_WeatherStat table
    op.create_table('Measurement_WeatherStat',
        sa.Column('Measurement_ID', sa.Integer, primary_key=True, nullable=False),
        sa.Column('Stream_ID', sa.Integer, sa.ForeignKey('Stream.Stream_ID'), nullable=False, default=0),
        sa.Column('Device_ID', sa.String(50), sa.ForeignKey('Device.Device_ID'), nullable=False, default=""),
        sa.Column('Type_ID', sa.Integer, sa.ForeignKey('Measurement_Type.Type_ID'), nullable=False, default=0),
        sa.Column('Data_Count', sa.Integer, nullable=False, default=0),
        sa.Column('Value', sa.Float, nullable=True, default=None),
        sa.Column('State', sa.Boolean, nullable=True, default=None),
        sa.Column('Min', sa.Float, nullable=True, default=None),
        sa.Column('Max', sa.Float, nullable=True, default=None),
        sa.Column('Avg', sa.Float, nullable=True, default=None),
        sa.Column('Deviation', sa.Float, nullable=True, default=None),
        sa.Column('Create_Time', sa.TIMESTAMP(timezone=True), nullable=False)
    )

    # Settings table
    op.create_table('Settings',
        sa.Column('Settings_ID', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('Device_ID', sa.String(50), sa.ForeignKey('Device.Device_ID'), nullable=False, default=""),
        sa.Column('Type_ID', sa.Integer, sa.ForeignKey('Measurement_Type.Type_ID'), nullable=False, default=0),
        sa.Column('Value', sa.Integer, nullable=False, default=0),
        sa.Column('Create_Time', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    )

    # RAW_Data table
    op.create_table('RAW_Data',
        sa.Column('RAW_Data_ID', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('Clent_IP', sa.String, nullable=True, default=None),
        sa.Column('RAW_Data', sa.JSON, nullable=True, default=None),
        sa.Column('Create_Time', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    )

    # Service_LOG table
    op.create_table('Service_LOG',
        sa.Column('Service_LOG_ID', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('Service', sa.String(100), nullable=False, default=""),
        sa.Column('Status', sa.Boolean, nullable=False, default=False, server_default=text('false')),
        sa.Column('Update_Time', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    )

    # Pass
    pass

# Downgrade DataBase
def downgrade() -> None:
    
    # Drop All Tables
    op.drop_table('Service_LOG')
    op.drop_table('RAW_Data')
    op.drop_table('Settings')
    op.drop_table('Measurement_WeatherStat')
    op.drop_table('Parameter')
    op.drop_table('Measurement_Type')
    op.drop_table('Device')
    op.drop_table('Version')
    op.drop_table('Stream')
    op.drop_table('Modem')
    op.drop_table('Model')
    op.drop_table('Manufacturer')
    op.drop_table('SIM')
    op.drop_table('Operator')

    # Pass
    pass
