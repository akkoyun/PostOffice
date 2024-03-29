# Setup Root Path
import sys
sys.path.append('/root/PostOffice/')

# Import Packages
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, JSON, LargeBinary
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from Setup.Database import Base, DB_Engine

# [A] Model Database Model
class Model(Base):

	# Define Table Name
	__tablename__ = "Model"

	# Define Columns
	Model_ID = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
	Model_Name = Column(String(), nullable=False)

# [B] Manufacturer Database Model
class Manufacturer(Base):

	# Define Table Name
	__tablename__ = "Manufacturer"

	# Define Columns
	Manufacturer_ID = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
	Manufacturer_Name = Column(String(), nullable=False)

# [C] Modem Database Model
class Modem(Base):

	# Define Table Name
	__tablename__ = "Modem"

	# Define Columns
	IMEI = Column(String(), primary_key=True, unique=True, nullable=False)
	Model_ID = Column(Integer, ForeignKey("Model.Model_ID", ondelete="CASCADE"), nullable=False)
	Manufacturer_ID = Column(Integer, ForeignKey("Manufacturer.Manufacturer_ID", ondelete="CASCADE"), nullable=False)
	Firmware = Column(String(), nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# [D] GSM_Operator Database Model
class GSM_Operator(Base):

	# Define Table Name
	__tablename__ = "GSM_Operator"

	# Define Columns
	Operator_ID = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
	MCC_ID = Column(Integer, nullable=False)
	MCC_ISO = Column(String(), nullable=False)
	MCC_Country_Name = Column(String(), nullable=False)
	MCC_Country_Code = Column(Integer, nullable=True)
	MCC_Country_Flag_Image_URL = Column(String(), nullable=True)
	MNC_ID = Column(Integer, nullable=False)
	MNC_Brand_Name = Column(String(), nullable=False)
	MNC_Operator_Name = Column(String(), nullable=False)
	MNC_Operator_Image_URL = Column(String(), nullable=True)

# [E] SIM Database Model
class SIM(Base):

	# Define Table Name
	__tablename__ = "SIM"

	# Define Columns
	ICCID = Column(String(), primary_key=True, unique=True, nullable=False)
	Operator_ID = Column(Integer, ForeignKey("GSM_Operator.Operator_ID", ondelete="CASCADE"), nullable=False)
	GSM_Number = Column(String(), nullable=True)
	Static_IP = Column(String(), nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# [F] Version Database Model
class Version(Base):

	# Define Table Name
	__tablename__ = "Version"

	# Define Columns
	Version_ID = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
	Device_ID = Column(String(), nullable=True)
	Firmware = Column(String(), nullable=True)
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# [G] Status Database Model
class Status(Base):

	# Define Table Name
	__tablename__ = "Status"

	# Define Columns
	Status_ID = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
	Description = Column(String(), nullable=False)

# [H] Device Database Model
class Device(Base):

	# Define Table Name
	__tablename__ = "Device"

	# Define Columns
	Device_ID = Column(String(), primary_key=True, unique=True, nullable=False)
	Status_ID = Column(Integer, ForeignKey("Status.Status_ID"), nullable=False)
	Version_ID = Column(Integer, ForeignKey("Version.Version_ID"), nullable=False)
	Model_ID = Column(Integer, ForeignKey("Model.Model_ID"), nullable=False)
	Project_ID = Column(Integer, ForeignKey("Project.Project_ID"), nullable=True)
	IMEI = Column(String(), ForeignKey("Modem.IMEI"), nullable=False)
	Last_Connection = Column(TIMESTAMP(timezone=True), nullable=True)
	Last_IP = Column(String(), nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# Project Database Model
class Project(Base):

	# Define Table Name
	__tablename__ = "Project"

	# Define Columns
	Project_ID = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
	Project_Name = Column(String(), nullable=False)
	Project_Description = Column(String(), nullable=False)

# [O] Data_Segment Database Model
class Data_Segment(Base):

	# Define Table Name
	__tablename__ = "Data_Segment"

	# Define Columns
	Segment_ID = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
	Description = Column(String(), nullable=False)

# [N] Data_Type Database Model
class Data_Type(Base):

	# Define Table Name
	__tablename__ = "Data_Type"

	# Define Columns
	Type_ID = Column(Integer, primary_key=True, unique=True, nullable=False)
	Description = Column(String(), nullable=False)
	Variable = Column(String(), nullable=True)
	Unit = Column(String(), nullable=True)
	Segment_ID = Column(Integer, ForeignKey("Data_Segment.Segment_ID"), nullable=False)

# [K] Parameter Database Model
class Parameter(Base):

	# Define Table Name
	__tablename__ = "Parameter"

	# Define Columns
	Parameter_ID = Column(Integer, primary_key=True, unique=True, nullable=False)
	Stream_ID = Column(Integer, ForeignKey("Stream.Stream_ID", ondelete="CASCADE"), nullable=False)
	Type_ID = Column(Integer, ForeignKey("Data_Type.Type_ID", ondelete="CASCADE"), nullable=False)
	Value = Column(Float, nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False)

# [L] Payload Database Model
class Payload(Base):

	# Define Table Name
	__tablename__ = "Payload"

	# Define Columns
	Measurement_ID = Column(Integer, primary_key=True, unique=True, nullable=False)
	Stream_ID = Column(Integer, ForeignKey("Stream.Stream_ID", ondelete="CASCADE"), nullable=False)
	Type_ID = Column(Integer, ForeignKey("Data_Type.Type_ID", ondelete="CASCADE"), nullable=False)
	Value = Column(Float, nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# [J] Stream Database Model
class Stream(Base):

	# Define Table Name
	__tablename__ = "Stream"

	# Define Columns
	Stream_ID = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
	Device_ID = Column(String(), ForeignKey("Device.Device_ID", ondelete="CASCADE"), nullable=False)
	ICCID = Column(String(), ForeignKey("SIM.ICCID"), nullable=False)
	Client_IP = Column(String, nullable=True)
	Device_Time = Column(TIMESTAMP(timezone=True), nullable=False)
	Stream_Time = Column(TIMESTAMP(timezone=True), nullable=False)
	RAW_Data = Column(JSON, nullable=True)
	Size = Column(Integer, nullable=True)

# Service_LOG Database Model
class Service_LOG(Base):

	# Define Table Name
	__tablename__ = "Service_LOG"

	# Define Columns
	Service_LOG_ID = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
	Service = Column(String(), nullable=False)
	Status = Column(Boolean, nullable=False, default=False)
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# Calibration Database Model
class Calibration(Base):

	# Define Table Name
	__tablename__ = "Calibration"

	# Define Columns
	Calibration_ID = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
	Device_ID = Column(String(), ForeignKey("Device.Device_ID", ondelete="CASCADE"), nullable=False)
	Type_ID = Column(Integer, ForeignKey("Data_Type.Type_ID", ondelete="CASCADE"), nullable=False)
	Gain = Column(Float, nullable=False, server_default="1")
	Offset = Column(Float, nullable=False, server_default="0")
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# Firmware Database Model
class Firmware(Base):

	# Define Table Name
	__tablename__ = "Firmware"

	# Define Columns
	Firmware_ID = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
	Version_ID = Column(Integer, ForeignKey("Version.Version_ID", ondelete="CASCADE"), nullable=False)
	File_Name = Column(String(), nullable=True)
	Size = Column(Integer, nullable=True)
	Title = Column(String(), nullable=True)
	Description = Column(String(), nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# View Models

# Payload_Measurement Database Model
class Payload_Measurement(Base):

	# Define Table Name
	__tablename__ = 'Payload_Measurement' 
	__table_args__ = {'autoload': True, 'autoload_with': DB_Engine}

	# Define Columns
	Measurement_ID = Column(Integer, primary_key=True)
	Device_ID = Column(String())
	Stream_ID = Column(Integer)
	Variable = Column(String())
	Value = Column(Float)
	Create_Time = Column(TIMESTAMP(timezone=True))
	Max = Column(Float)
	Min = Column(Float)
	Max_Time = Column(TIMESTAMP(timezone=True))
	Min_Time = Column(TIMESTAMP(timezone=True))
	PreviousValue = Column(Float)
	Trend = Column(Integer)

# Parameter_Measurement Database Model
class Parameter_Measurement(Base):

	# Define Table Name
	__tablename__ = 'Parameter_Measurement' 
	__table_args__ = {'autoload': True, 'autoload_with': DB_Engine}

	# Define Columns
	Parameter_ID = Column(Integer, primary_key=True)
	Device_ID = Column(String())
	Stream_ID = Column(Integer)
	Variable = Column(String())
	Value = Column(Float)
	Create_Time = Column(TIMESTAMP(timezone=True))
	Max = Column(Float)
	Min = Column(Float)
	Max_Time = Column(TIMESTAMP(timezone=True))
	Min_Time = Column(TIMESTAMP(timezone=True))
	PreviousValue = Column(Float)
	Trend = Column(Integer)

# Rain_Calculate Database Model
class Rain_Calculate(Base):

		# Define Table Name
	__tablename__ = 'Rain_Calculate' 
	__table_args__ = {'autoload': True, 'autoload_with': DB_Engine}

	# Define Columns
	Device_ID = Column(String(), primary_key=True)
	R_1 = Column(Integer)
	R_24 = Column(Integer)
	R_48 = Column(Integer)
	R_168 = Column(Integer)

# Calibration_View Database Model
class Calibration_View(Base):

		# Define Table Name
	__tablename__ = 'Calibration_View' 
	__table_args__ = {'autoload': True, 'autoload_with': DB_Engine}

	# Define Columns
	Device_ID = Column(String(), primary_key=True)
	Variable = Column(String())
	Gain = Column(Float)
	Offset = Column(Float)
	Create_Time = Column(TIMESTAMP(timezone=True))
