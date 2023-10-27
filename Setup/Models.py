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
	MCC_ID = Column(Integer, nullable=False, default=0)
	MCC_ISO = Column(String(3), nullable=False, default="")
	MCC_Country_Name = Column(String(50), nullable=False, default="")
	MCC_Country_Code = Column(Integer, nullable=True, default=None)
	MCC_Country_Flag_Image_URL = Column(String(255), nullable=True, default=None)
	MNC_ID = Column(Integer, nullable=False, default=0)
	MNC_Brand_Name = Column(String(50), nullable=False, default="")
	MNC_Operator_Name = Column(String(50), nullable=False, default="")
	MNC_Operator_Image_URL = Column(String(255), nullable=True, default=None)

	# Relationship Definition
	Def_SIM = relationship("SIM", backref="Operator")

# SIM Database Model
class SIM(Base):

	# Define Table Name
	__tablename__ = "SIM"

	# Define Columns
	ICCID = Column(String(20), primary_key=True, nullable=False)
	Operator_ID = Column(Integer, ForeignKey('Operator.Operator_ID'), nullable=False, default=0)
	GSM_Number = Column(String(15), nullable=True, default=None)
	Static_IP = Column(String(15), nullable=True, default=None)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# Manufacturer Database Model
class Manufacturer(Base):

	# Define Table Name
	__tablename__ = "Manufacturer"

	# Define Columns
	Manufacturer_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Manufacturer = Column(String(50), nullable=False, default="")

	# Relationship Definition
	Def_Modem = relationship("Modem", backref="Manufacturer")

# Model Database Model
class Model(Base):

	# Define Table Name
	__tablename__ = "Model"

	# Define Columns
	Model_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Model = Column(String(50), nullable=False, default="")

	# Relationship Definition
	Def_Modem = relationship("Modem", backref="Model")

# Modem Database Model
class Modem(Base):

	# Define Table Name
	__tablename__ = "Modem"

	# Define Columns
	IMEI = Column(String(20), primary_key=True, nullable=False)
	Manufacturer_ID = Column(Integer, ForeignKey('Manufacturer.Manufacturer_ID'), nullable=False, default=0)
	Model_ID = Column(Integer, ForeignKey('Model.Model_ID'), nullable=False, default=0)
	Firmware = Column(String(10), nullable=True, default=None)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# Stream Database Model
class Stream(Base):

	# Define Table Name
	__tablename__ = "Stream"

	# Define Columns
	Stream_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Device_ID = Column(String(50), ForeignKey('Device.Device_ID'), nullable=False, default="")
	IMEI = Column(String(20), ForeignKey('Modem.IMEI'), nullable=False, default="")
	ICCID = Column(String(20), ForeignKey('SIM.ICCID'), nullable=False, default="")
	RSSI = Column(Integer, nullable=True, default=None)
	TAC = Column(Integer, nullable=True, default=None)
	LAC = Column(Integer, nullable=True, default=None)
	Cell_ID = Column(Integer, nullable=True, default=None)
	Device_IP = Column(String, nullable=True, default=None)
	Connection_Time = Column(Integer, nullable=True, default=None)
	Size = Column(Integer, nullable=True, default=None)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# Version Database Model
class Version(Base):

	# Define Table Name
	__tablename__ = "Version"

	# Define Columns
	Version_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Device_ID = Column(String(50), nullable=False, default="")
	Firmware = Column(String(10), nullable=True, default=None)
	Hardware = Column(String(10), nullable=True, default=None)
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

	# Relationship Definition
	Def_Device = relationship("Device", backref="Def_Version")

# Device Database Model
class Device(Base):

	# Define Table Name
	__tablename__ = "Device"

	# Define Columns
	Device_ID = Column(String(50), primary_key=True, nullable=False)
	Version_ID = Column(Integer, ForeignKey('Version.Version_ID'), nullable=False, default=0)
	Model_ID = Column(Integer, nullable=False, default=0)
	Status = Column(Boolean, nullable=False, default=False, server_default=text('false'))
	Create_Date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# Measurement_Type Database Model
class Measurement_Type(Base):

	# Define Table Name
	__tablename__ = "Measurement_Type"

	# Define Columns
	Type_ID = Column(Integer, primary_key=True, nullable=False)
	Description = Column(String(255), nullable=False, default="")
	Variable = Column(String(10), nullable=True, default=None)
	Unit = Column(String(10), nullable=True, default=None)
	Segment = Column(Integer, nullable=False, default=0)

	# Relationship Definition
	Def_Measurement_Device = relationship("Parameter", backref="Def_Measurement_Type")
	Def_Measurement_WeatherStat = relationship("Measurement_WeatherStat", backref="Def_Measurement_Type")

# Parameter Database Model
class Parameter(Base):

	# Define Table Name
	__tablename__ = "Parameter"

	# Define Columns
	Parameter_ID = Column(Integer, primary_key=True, nullable=False)
	Stream_ID = Column(Integer, ForeignKey('Stream.Stream_ID'), nullable=False, default=0)
	Type_ID = Column(Integer, ForeignKey('Measurement_Type.Type_ID'), nullable=False, default=0)
	Value = Column(Float, nullable=True, default=None)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False)

# Measurement_WeatherStat Database Model
class Measurement_WeatherStat(Base):

	# Define Table Name
	__tablename__ = "Measurement_WeatherStat"

	# Define Columns
	Measurement_ID = Column(Integer, primary_key=True, nullable=False)
	Stream_ID = Column(Integer, ForeignKey('Stream.Stream_ID'), nullable=False, default=0)
	Device_ID = Column(String(50), ForeignKey('Device.Device_ID'), nullable=False, default="")
	Type_ID = Column(Integer, ForeignKey('Measurement_Type.Type_ID'), nullable=False, default=0)
	Data_Count = Column(Integer, nullable=False, default=0)
	Value = Column(Float, nullable=True, default=None)
	State = Column(Boolean, nullable=True, default=None)
	Min = Column(Float, nullable=True, default=None)
	Max = Column(Float, nullable=True, default=None)
	Avg = Column(Float, nullable=True, default=None)
	Deviation = Column(Float, nullable=True, default=None)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False)

# Settings Database Model
class Settings(Base):

	# Define Table Name
	__tablename__ = "Settings"

	# Define Columns
	Settings_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Device_ID = Column(String(50), ForeignKey('Device.Device_ID'), nullable=False, default="")
	Type_ID = Column(Integer, ForeignKey('Measurement_Type.Type_ID'), nullable=False, default=0)
	Value = Column(Integer, nullable=False, default=0)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

	# Relationship Definition
	Def_Device = relationship("Device", back_populates="Def_Settings")

# RAW_Data Database Model
class RAW_Data(Base):

	# Define Table Name
	__tablename__ = "RAW_Data"

	# Define Columns
	RAW_Data_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Clent_IP = Column(String, nullable=True, default=None)
	RAW_Data = Column(JSON, nullable=True, default=None)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# Service_LOG Database Model
class Service_LOG(Base):

	# Define Table Name
	__tablename__ = "Service_LOG"

	# Define Columns
	Service_LOG_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Service = Column(String(100), nullable=False, default="")
	Status = Column(Boolean, nullable=False, default=False, server_default=text('false'))
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
