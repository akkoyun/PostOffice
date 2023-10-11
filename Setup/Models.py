from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .Database import Base, SessionLocal, DB_Engine

# GSM_MNC Database Model
class GSM_MNC(Base):

	# Define Table Name
	__tablename__ = "GSM_MNC"

	# Define Colomns
	MNC_Row_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	MNC_ID = Column(Integer, nullable=False)
	MNC_Name = Column(String, nullable=False)

	# Define Relationships
	Relation_SIM = relationship("SIM", back_populates="Relation_MNC_ID", cascade="all, delete-orphan")

# GSM_MCC Database Model
class GSM_MCC(Base):

	# Define Table Name
	__tablename__ = "GSM_MCC"

	# Define Colomns
	MCC_Row_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	MCC_ID = Column(Integer, nullable=False)
	MCC_Name = Column(String, nullable=False)

	# Define Relationships
	Relation_SIM = relationship("SIM", back_populates="Relation_MCC_ID", cascade="all, delete-orphan")

# SIM Database Model
class SIM(Base):

	# Define Table Name
	__tablename__ = "SIM"

	# Define Colomns
	SIM_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Device_ID = Column(String, nullable=False)
	SIM_ICCID = Column(String, nullable=False)
	MCC_ID = Column(Integer, ForeignKey('GSM_MCC.MCC_ID'), nullable=False)
	MNC_ID = Column(Integer, ForeignKey('GSM_MNC.MNC_ID'), nullable=False)
	SIM_Number = Column(String, nullable=True)
	SIM_IP = Column(String, nullable=True)
	SIM_Status = Column(Boolean, nullable=False, server_default=text('false'))
	SIM_Create_Date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

	# Define Relationships
	Relation_MNC_ID = relationship("GSM_MNC", back_populates="Relation_SIM")
	Relation_MCC_ID = relationship("GSM_MCC", back_populates="Relation_SIM")
	Relation_SIM_ID = relationship("Connection", back_populates="Relation_SIM", cascade="all, delete-orphan")

# Connection Database Model
class Connection(Base):

	# Define Table Name
	__tablename__ = "Connection"

	# Define Colomns
	Connection_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Device_ID = Column(String, ForeignKey('Data_Stream.Device_ID'), nullable=False)
	SIM_ID = Column(Integer, ForeignKey('SIM.SIM_ID'), nullable=False)
	Connection_RSSI = Column(Integer, nullable=True)
	Connection_IP = Column(String, nullable=True)
	Connection_Time	= Column(Integer, nullable=True)
	Connection_Data_Size = Column(Integer, nullable=True)
	Connection_Create_Date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

	# Define Relationships
	Relation_Data_Stream = relationship("Data_Stream", back_populates="Relation_Connection")
	Relation_SIM = relationship("SIM", back_populates="Relation_SIM_ID", cascade="all, delete-orphan")

# Module_Type Database Model
class Module_Type(Base):

	# Define Table Name
	__tablename__ = "Module_Type"

	# Define Colomns
	Module_Type_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Module_Type_Name = Column(String, nullable=False)

	# Define Relationships
	Relation_IoT_Module = relationship("IoT_Module", back_populates="Relation_Module_Type_ID", cascade="all, delete-orphan")

# Module_Manufacturer Database Model
class Module_Manufacturer(Base):

	# Define Table Name
	__tablename__ = "Module_Manufacturer"

	# Define Colomns
	Module_Manufacturer_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Module_Manufacturer_Name = Column(String, nullable=False)

	# Define Relationships
	Relation_IoT_Module = relationship("IoT_Module", back_populates="Relation_Module_Manufacturer_ID", cascade="all, delete-orphan")

# Module_Model Database Model
class Module_Model(Base):

	# Define Table Name
	__tablename__ = "Module_Model"

	# Define Colomns
	Module_Model_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Module_Model_Name = Column(String, nullable=False)

	# Define Relationships
	Relation_IoT_Module = relationship("IoT_Module", back_populates="Relation_Module_Model_ID", cascade="all, delete-orphan")

# IoT_Module Database Model
class IoT_Module(Base):

	# Define Table Name
	__tablename__ = "IoT_Module"

	# Define Colomns
	Module_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Device_ID = Column(String, ForeignKey('Data_Stream.Device_ID'), nullable=False)
	Module_Type_ID = Column(Integer, ForeignKey("Module_Type.Module_Type_ID"), nullable=False)
	Module_Firmware = Column(String, nullable=True)
	Module_IMEI = Column(String, nullable=True)
	Module_Serial = Column(String, nullable=True)
	Module_Manufacturer_ID = Column(Integer, ForeignKey("Module_Manufacturer.Module_Manufacturer_ID"), nullable=False)
	Module_Model_ID = Column(Integer, ForeignKey("Module_Model.Module_Model_ID"), nullable=False)
	Module_Create_Date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

	# Define Relationships
	Relation_Module_Type_ID = relationship("Module_Type", back_populates="Relation_IoT_Module")
	Relation_Module_Manufacturer_ID = relationship("Module_Manufacturer", back_populates="Relation_IoT_Module")
	Relation_Module_Model_ID = relationship("Module_Model", back_populates="Relation_IoT_Module")
	Relation_Data_Stream = relationship("Data_Stream", back_populates="Relation_IoT_Module")

# Location Database Model
class Location(Base):

	# Define Table Name
	__tablename__ = "Location"

	# Define Colomns
	Location_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Device_ID = Column(String, ForeignKey('Data_Stream.Device_ID'), nullable=False)
	Location_TAC = Column(Integer, nullable=True)
	Location_LAC = Column(Integer, nullable=True)
	Location_Cell_ID = Column(Integer, nullable=True)
	Location_Latitude = Column(float, nullable=True)
	Location_Longitude = Column(float, nullable=True)
	Location_Date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

	# Define Relationships
	Relation_Data_Stream = relationship("Data_Stream", back_populates="Relation_Location")

# Register Database Model
class Register(Base):

	# Define Table Name
	__tablename__ = "Register"

	# Define Colomns
	Register_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Device_ID = Column(String, ForeignKey('Data_Stream.Device_ID'), nullable=False)
	Register_Status = Column(Integer, nullable=False)
	Register_Create_Date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

	# Define Relationships
	Relation_Data_Stream = relationship("Data_Stream", back_populates="Relation_Register")

# Data_Stream Database Model
class Data_Stream(Base):

	# Define Table Name
	__tablename__ = "Data_Stream"

	# Define Colomns
	Data_Stream_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Device_ID = Column(String, ForeignKey('Device.Device_ID'), nullable=False)
	Data_Stream_Create_Date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

	# Define Relationships
	Relation_Location = relationship("Location", back_populates="Relation_Data_Stream")
	Relation_Register = relationship("Register", back_populates="Relation_Data_Stream")
	Relation_IoT_Module = relationship("IoT_Module", back_populates="Relation_Data_Stream")
	Relation_Connection = relationship("Connection", back_populates="Relation_Data_Stream")
	Relation_Device = relationship("Device", back_populates="Relation_Data_Stream")

# Version Database Model
class Version(Base):

	# Define Table Name
	__tablename__ = "Version"

	# Define Colomns
	Version_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Device_ID = Column(String, ForeignKey("Device.Device_ID"), nullable=False)
	Version_Firmware = Column(String, nullable=True)
	Version_Hardware = Column(String, nullable=True)
	Version_Update_Date = Column(TIMESTAMP(timezone=True), nullable=False)

	# Define Relationships
	Relation_Device = relationship("Device", back_populates="Relation_Version", cascade="all, delete-orphan")

# Device Database Model
class Device(Base):

	# Define Table Name
	__tablename__ = "Device"

	# Define Colomns
	Device_ID = Column(String, primary_key=True, nullable=False)
	Device_Status = Column(Boolean, nullable=False)
	Device_Create_Date = Column(TIMESTAMP(timezone=True), nullable=False)

	# Define Relationships
	Relation_Data_Stream = relationship("Data_Stream", back_populates="Relation_Device", cascade="all, delete-orphan")
	Relation_Settings = relationship("Settings", back_populates="Relation_Device")
	Relation_Version = relationship("Version", back_populates="Relation_Device")

# Settings Database Model
class Settings(Base):

	# Define Table Name
	__tablename__ = "Settings"

	# Define Colomns
	Settings_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Device_ID = Column(String, ForeignKey("Device.Device_ID"), nullable=False)
	Publish_Register = Column(Integer, nullable=False)
	Stop_Register = Column(Integer, nullable=False)
	Settings_Status = Column(Boolean, nullable=False)
	Settings_Create_Date = Column(TIMESTAMP(timezone=True), nullable=False)

	# Define Relationships
	Relation_Device = relationship("Device", back_populates="Relation_Settings", cascade="all, delete-orphan")

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

	# Define Relationships
	Relation_Measurement = relationship("Measurement", back_populates="Relation_Measurement_Type_ID", cascade="all, delete-orphan")

# Measurement Database Model
class Measurement(Base):

	# Define Table Name
	__tablename__ = "Measurement"

	# Define Colomns
	Measurement_ID = Column(Integer, primary_key=True, nullable=False)
	Data_Stream_ID = Column(Integer, ForeignKey('Data_Stream.Data_Stream_ID'), nullable=False)
	Measurement_Type_ID = Column(Integer, ForeignKey('Measurement_Type.Measurement_Type_ID'), nullable=False)
	Measurement_Data_Count = Column(Integer, nullable=False)
	Measurement_Value = Column(float, nullable=True)
	Measurement_State = Column(Boolean, nullable=True)
	Measurement_Min = Column(float, nullable=True)
	Measurement_Max = Column(float, nullable=True)
	Measurement_Avg = Column(float, nullable=True)
	Measurement_Q1 = Column(float, nullable=True)
	Measurement_Q2 = Column(float, nullable=True)
	Measurement_Q3 = Column(float, nullable=True)
	Measurement_Deviation = Column(float, nullable=True)
	Measurement_Create_Date = Column(TIMESTAMP(timezone=True), nullable=False)

	# Define Relationships
	Relation_Measurement_Type_ID = relationship("Measurement_Type", back_populates="Relation_Measurement")
	Relation_Data_Stream = relationship("Data_Stream", back_populates="Relation_Measurement")

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
	RAW_Data = Column(String, nullable=True)
	RAW_Data_Create_Date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
