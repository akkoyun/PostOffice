# Setup Library
import sys
sys.path.append('/root/PostOffice/')

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, JSON
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .Database import Base

# Operator Database Model
class Operator(Base):

	# Define Table Name
	__tablename__ = "Operator"

	# Define Columns
	Operator_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	MCC_ID = Column(Integer, nullable=False)
	MCC_ISO = Column(String(), nullable=False)
	MCC_Country_Name = Column(String(), nullable=False)
	MCC_Country_Code = Column(Integer, nullable=True)
	MCC_Country_Flag_Image_URL = Column(String(), nullable=True)
	MNC_ID = Column(Integer, nullable=False)
	MNC_Brand_Name = Column(String(), nullable=False)
	MNC_Operator_Name = Column(String(), nullable=False)
	MNC_Operator_Image_URL = Column(String(), nullable=True)

	# Relationship Definition
	Def_SIM = relationship("SIM", backref="Operator")

# SIM Database Model
class SIM(Base):

	# Define Table Name
	__tablename__ = "SIM"

	# Define Columns
	ICCID = Column(String(), primary_key=True, nullable=False)
	Operator_ID = Column(Integer, ForeignKey('Operator.Operator_ID'), nullable=False)
	GSM_Number = Column(String(), nullable=True)
	Static_IP = Column(String(), nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# Manufacturer Database Model
class Manufacturer(Base):

	# Define Table Name
	__tablename__ = "Manufacturer"

	# Define Columns
	Manufacturer_ID = Column(Integer, primary_key=True, nullable=False)
	Manufacturer = Column(String(), nullable=False)

	# Relationship Definition
	Def_Modem = relationship("Modem", backref="Manufacturer")

# Model Database Model
class Model(Base):

	# Define Table Name
	__tablename__ = "Model"

	# Define Columns
	Model_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Model = Column(String(), nullable=False)

	# Relationship Definition
	Def_Modem = relationship("Modem", backref="Model")

# Modem Database Model
class Modem(Base):

	# Define Table Name
	__tablename__ = "Modem"

	# Define Columns
	IMEI = Column(String(), primary_key=True, nullable=False)
	Manufacturer_ID = Column(Integer, ForeignKey('Manufacturer.Manufacturer_ID'), nullable=False)
	Model_ID = Column(Integer, ForeignKey('Model.Model_ID'), nullable=False)
	Firmware = Column(String(), nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# Stream Database Model
class Stream(Base):

	# Define Table Name
	__tablename__ = "Stream"

	# Define Columns
	Stream_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Device_ID = Column(String(), ForeignKey('Device.Device_ID'), nullable=False)
	IMEI = Column(String(), ForeignKey('Modem.IMEI'), nullable=False)
	ICCID = Column(String(), ForeignKey('SIM.ICCID'), nullable=False)
	RSSI = Column(Integer, nullable=True)
	TAC = Column(Integer, nullable=True)
	LAC = Column(Integer, nullable=True)
	Cell_ID = Column(Integer, nullable=True)
	Device_IP = Column(String, nullable=True)
	Connection_Time = Column(Integer, nullable=True)
	Size = Column(Integer, nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# Version Database Model
class Version(Base):

	# Define Table Name
	__tablename__ = "Version"

	# Define Columns
	Version_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Device_ID = Column(String(), nullable=False)
	Firmware = Column(String(), nullable=True)
	Hardware = Column(String(), nullable=True)
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

	# Relationship Definition
	Def_Device = relationship("Device", backref="Def_Version")

# Device Database Model
class Device(Base):

	# Define Table Name
	__tablename__ = "Device"

	# Define Columns
	Device_ID = Column(String(), primary_key=True, nullable=False)
	Version_ID = Column(Integer, ForeignKey('Version.Version_ID'), nullable=False)
	Model_ID = Column(Integer, nullable=False)
	Status = Column(Boolean, nullable=False)
	Create_Date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# Measurement_Type Database Model
class Measurement_Type(Base):

	# Define Table Name
	__tablename__ = "Measurement_Type"

	# Define Columns
	Type_ID = Column(Integer, primary_key=True, nullable=False)
	Description = Column(String(), nullable=False)
	Variable = Column(String(), nullable=True)
	Unit = Column(String(), nullable=True)
	Segment = Column(Integer, nullable=False)

	# Relationship Definition
	Def_Measurement_Device = relationship("Parameter", backref="Def_Measurement_Type")
	Def_Measurement_WeatherStat = relationship("Measurement_WeatherStat", backref="Def_Measurement_Type")

# Parameter Database Model
class Parameter(Base):

	# Define Table Name
	__tablename__ = "Parameter"

	# Define Columns
	Parameter_ID = Column(Integer, primary_key=True, nullable=False)
	Stream_ID = Column(Integer, ForeignKey('Stream.Stream_ID'), nullable=False)
	Type_ID = Column(Integer, ForeignKey('Measurement_Type.Type_ID'), nullable=False)
	Value = Column(Float, nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False)

# Measurement_WeatherStat Database Model
class Measurement_WeatherStat(Base):

	# Define Table Name
	__tablename__ = "Measurement_WeatherStat"

	# Define Columns
	Measurement_ID = Column(Integer, primary_key=True, nullable=False)
	Stream_ID = Column(Integer, ForeignKey('Stream.Stream_ID'), nullable=False)
	Device_ID = Column(String(), ForeignKey('Device.Device_ID'), nullable=False)
	Type_ID = Column(Integer, ForeignKey('Measurement_Type.Type_ID'), nullable=False)
	Data_Count = Column(Integer, nullable=False)
	Value = Column(Float, nullable=True)
	State = Column(Boolean, nullable=True)
	Min = Column(Float, nullable=True)
	Max = Column(Float, nullable=True)
	Avg = Column(Float, nullable=True)
	Deviation = Column(Float, nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False)

# Settings Database Model
class Settings(Base):

	# Define Table Name
	__tablename__ = "Settings"

	# Define Columns
	Settings_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Device_ID = Column(String(), ForeignKey('Device.Device_ID'), nullable=False)
	Type_ID = Column(Integer, ForeignKey('Measurement_Type.Type_ID'), nullable=False)
	Value = Column(Integer, nullable=False)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# RAW_Data Database Model
class RAW_Data(Base):

	# Define Table Name
	__tablename__ = "RAW_Data"

	# Define Columns
	RAW_Data_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Clent_IP = Column(String, nullable=True)
	RAW_Data = Column(JSON, nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# Service_LOG Database Model
class Service_LOG(Base):

	# Define Table Name
	__tablename__ = "Service_LOG"

	# Define Columns
	Service_LOG_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Service = Column(String(), nullable=False)
	Status = Column(Boolean, nullable=False, default=False)
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
