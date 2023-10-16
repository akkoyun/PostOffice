from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, UniqueConstraint, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .Database import Base, SessionLocal, DB_Engine

# GSM_MNC Database Model
class GSM_MNC(Base):

	# Define Table Name
	__tablename__ = "GSM_MNC"

	# Define Colomns
	MNC_ID = Column(Integer, primary_key=True, nullable=False)
	MNC_Name = Column(String, nullable=False)

# GSM_MCC Database Model
class GSM_MCC(Base):

	# Define Table Name
	__tablename__ = "GSM_MCC"

	# Define Colomns
	MCC_ID = Column(Integer, primary_key=True, nullable=False)
	MCC_Name = Column(String, nullable=False)

# SIM Database Model
class SIM(Base):

	# Define Table Name
	__tablename__ = "SIM"

	# Define Colomns
	SIM_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Device_ID = Column(String, nullable=False)
	SIM_ICCID = Column(String, nullable=False)
	MCC_ID = Column(Integer, nullable=False)
	MNC_ID = Column(Integer, nullable=False)
	SIM_Number = Column(String, nullable=True)
	SIM_IP = Column(String, nullable=True)
	SIM_Status = Column(Boolean, nullable=False, server_default=text('false'))
	SIM_Create_Date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# Connection Database Model
class Connection(Base):

	# Define Table Name
	__tablename__ = "Connection"

	# Define Colomns
	Connection_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Device_ID = Column(String, nullable=False)
	SIM_ID = Column(Integer, nullable=False)
	Connection_RSSI = Column(Integer, nullable=True)
	Connection_IP = Column(String, nullable=True)
	Connection_Time	= Column(Integer, nullable=True)
	Connection_Data_Size = Column(Integer, nullable=True)
	Connection_Create_Date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# Module_Type Database Model
class Module_Type(Base):

	# Define Table Name
	__tablename__ = "Module_Type"

	# Define Colomns
	Module_Type_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Module_Type_Name = Column(String, nullable=False)

# Module_Manufacturer Database Model
class Module_Manufacturer(Base):

	# Define Table Name
	__tablename__ = "Module_Manufacturer"

	# Define Colomns
	Module_Manufacturer_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Module_Manufacturer_Name = Column(String, nullable=False)

# Module_Model Database Model
class Module_Model(Base):

	# Define Table Name
	__tablename__ = "Module_Model"

	# Define Colomns
	Module_Model_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Module_Model_Name = Column(String, nullable=False)

# IoT_Module Database Model
class IoT_Module(Base):

	# Define Table Name
	__tablename__ = "IoT_Module"

	# Define Colomns
	Module_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Device_ID = Column(String, nullable=False)
	Module_Type_ID = Column(Integer, nullable=False)
	Module_Firmware = Column(String, nullable=True)
	Module_IMEI = Column(String, nullable=True)
	Module_Serial = Column(String, nullable=True)
	Module_Manufacturer_ID = Column(Integer, nullable=False)
	Module_Model_ID = Column(Integer, nullable=False)
	Module_Create_Date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# Location Database Model
class Location(Base):

	# Define Table Name
	__tablename__ = "Location"

	# Define Colomns
	Location_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Device_ID = Column(String, nullable=False)
	Location_TAC = Column(Integer, nullable=True)
	Location_LAC = Column(Integer, nullable=True)
	Location_Cell_ID = Column(Integer, nullable=True)
	Location_Latitude = Column(Float, nullable=True)
	Location_Longitude = Column(Float, nullable=True)
	Location_Date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# Register Database Model
class Register(Base):

	# Define Table Name
	__tablename__ = "Register"

	# Define Colomns
	Register_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Device_ID = Column(String, nullable=False)
	Register_Status = Column(Integer, nullable=False)
	Register_Create_Date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# Data_Stream Database Model
class Data_Stream(Base):

	# Define Table Name
	__tablename__ = "Data_Stream"

	# Define Colomns
	Data_Stream_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Device_ID = Column(String, nullable=False)
	Data_Stream_Create_Date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# Version Database Model
class Version(Base):

	# Define Table Name
	__tablename__ = "Version"

	# Define Colomns
	Version_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Device_ID = Column(String, nullable=False)
	Version_Firmware = Column(String, nullable=True)
	Version_Hardware = Column(String, nullable=True)
	Version_Update_Date = Column(TIMESTAMP(timezone=True), nullable=False)

# Device Database Model
class Device(Base):

	# Define Table Name
	__tablename__ = "Device"

	# Define Colomns
	Device_ID = Column(String, primary_key=True, nullable=False)
	Device_Status = Column(Boolean, nullable=False, default=False)
	Device_Data_Count = Column(Integer, nullable=False, default=0)
	Device_Create_Date = Column(TIMESTAMP(timezone=True), nullable=False)
	Device_Last_Online = Column(TIMESTAMP(timezone=True), nullable=False)

# Settings Database Model
class Settings(Base):

	# Define Table Name
	__tablename__ = "Settings"

	# Define Colomns
	Settings_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Device_ID = Column(String, nullable=False)
	Publish_Register = Column(Integer, nullable=False)
	Stop_Register = Column(Integer, nullable=False)
	Settings_Status = Column(Boolean, nullable=False)
	Settings_Create_Date = Column(TIMESTAMP(timezone=True), nullable=False)

# Measurement_Type Database Model
class Measurement_Type(Base):

	# Define Table Name
	__tablename__ = "Measurement_Type"

	# Define Colomns
	Measurement_Type_ID = Column(Integer, primary_key=True, nullable=False)
	Measurement_Type_Name = Column(String, nullable=False)
	Measurement_Type_Variable = Column(String, nullable=False)
	Measurement_Type_Unit = Column(String, nullable=False)
	Measurement_Type_Segment = Column(String, nullable=False)

# Measurement Database Model
class Measurement(Base):

	# Define Table Name
	__tablename__ = "Measurement"

	# Define Colomns
	Measurement_ID = Column(Integer, primary_key=True, nullable=False)
	Data_Stream_ID = Column(Integer, nullable=False)
	Measurement_Type_ID = Column(Integer, nullable=False)
	Measurement_Data_Count = Column(Integer, nullable=False)
	Measurement_Value = Column(Float, nullable=True)
	Measurement_State = Column(Boolean, nullable=True)
	Measurement_Min = Column(Float, nullable=True)
	Measurement_Max = Column(Float, nullable=True)
	Measurement_Avg = Column(Float, nullable=True)
	Measurement_Q1 = Column(Float, nullable=True)
	Measurement_Q2 = Column(Float, nullable=True)
	Measurement_Q3 = Column(Float, nullable=True)
	Measurement_Deviation = Column(Float, nullable=True)
	Measurement_Create_Date = Column(TIMESTAMP(timezone=True), nullable=False)

# RAW_Data Database Model
class RAW_Data(Base):

	# Define Table Name
	__tablename__ = "RAW_Data"

	# Define Colomns
	RAW_Data_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	RAW_Data_Device_ID = Column(String, nullable=True)
	RAW_Data_Company = Column(String, nullable=True)
	RAW_Data_Device = Column(String, nullable=True)
	RAW_Data_Command = Column(String, nullable=True)
	RAW_Data_IP = Column(String, nullable=True)
	RAW_Data = Column(JSON, nullable=True)
	RAW_Data_Valid = Column(Boolean, nullable=True, server_default=text('true'))
	RAW_Data_Create_Date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
