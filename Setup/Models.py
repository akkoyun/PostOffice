# Setup Root Path
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Import Packages
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, JSON, Index, UniqueConstraint
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from Setup.Database import Base

# [A] Model Database Model
class Model(Base):

	# Define Table Name
	__tablename__ = "Model"

	# Define Columns
	Model_ID = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
	Model_Name = Column(String(100), nullable=False)
	Model_Description = Column(String(255), nullable=True, server_default="No description")
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=text('now()'))

	# Define Relationships
	devices = relationship("Device", back_populates="model")
	modems = relationship("Modem", back_populates="model")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_model_name', 'Model_Name', unique=True),
	)

# [B] Manufacturer Database Model
class Manufacturer(Base):

	# Define Table Name
	__tablename__ = "Manufacturer"

	# Define Columns
	Manufacturer_ID = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
	Manufacturer_Name = Column(String(100), nullable=False)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=text('now()'))

	# Define Relationships
	devices = relationship("Device", back_populates="manufacturer")
	modems = relationship("Modem", back_populates="manufacturer")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_manufacturer_name', 'Manufacturer_Name'),
	)

# [C] Modem Database Model
class Modem(Base):

	# Define Table Name
	__tablename__ = "Modem"

	# Define Columns
	IMEI = Column(String(20), primary_key=True, unique=True, nullable=False)
	Model_ID = Column(Integer, ForeignKey("Model.Model_ID", ondelete="CASCADE"), nullable=False)
	Manufacturer_ID = Column(Integer, ForeignKey("Manufacturer.Manufacturer_ID", ondelete="CASCADE"), nullable=False)
	Firmware = Column(String(10), nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=text('now()'))

	# Define Relationships
	model = relationship("Model", back_populates="modems")
	manufacturer = relationship("Manufacturer", back_populates="modems")
	devices = relationship("Device", back_populates="modem")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_modem_imei', 'IMEI'),
		Index('idx_modem_model_id', 'Model_ID'),
		Index('idx_modem_manufacturer_id', 'Manufacturer_ID'),
	)

# [D] GSM_Operator Database Model
class GSM_Operator(Base):

	# Define Table Name
	__tablename__ = "GSM_Operator"

	# Define Columns
	Operator_ID = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
	MCC_ID = Column(Integer, nullable=False)
	MCC_ISO = Column(String(3), nullable=False)
	MCC_Country_Name = Column(String(100), nullable=False)
	MCC_Country_Code = Column(Integer, nullable=True)
	MCC_Country_Flag_Image_URL = Column(String(255), nullable=True)
	MNC_ID = Column(Integer, nullable=False)
	MNC_Brand_Name = Column(String(100), nullable=False)
	MNC_Operator_Name = Column(String(100), nullable=False)
	MNC_Operator_Image_URL = Column(String(255), nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=text('now()'))

	# Define Relationships
	sims = relationship("SIM", back_populates="operator")

	# Define Table Arguments
	__table_args__ = (
		UniqueConstraint('MCC_ID', 'MNC_ID', name='uix_mcc_mnc'),
		Index('idx_mcc_id', 'MCC_ID'),
		Index('idx_mnc_id', 'MNC_ID'),
		Index('idx_mcc_iso', 'MCC_ISO'),
		Index('idx_mnc_operator_name', 'MNC_Operator_Name'),
	)

# [E] SIM Database Model
class SIM(Base):

	# Define Table Name
	__tablename__ = "SIM"

	# Define Columns
	ICCID = Column(String(25), primary_key=True, unique=True, nullable=False)
	Operator_ID = Column(Integer, ForeignKey("GSM_Operator.Operator_ID", ondelete="CASCADE"), nullable=False)
	GSM_Number = Column(String(15), nullable=True)
	Status = Column(Boolean, nullable=False, server_default="1")
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=text('now()'))

	# Define Relationships
	streams = relationship("Stream", back_populates="sim")
	operator = relationship("GSM_Operator", back_populates="sims")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_iccid', 'ICCID'),
		Index('idx_operator_id', 'Operator_ID'),
		Index('idx_gsm_number', 'GSM_Number'),
	)

# [F] Version Database Model
class Version(Base):

	# Define Table Name
	__tablename__ = "Version"

	# Define Columns
	Version_ID = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
	Firmware = Column(String(20), nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=text('now()'))

	# Define Relationships
	devices = relationship("Device", back_populates="version")
	firmwares = relationship("Firmware", back_populates="version")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_firmware', 'Firmware'),
	)

# [G] Status Database Model
class Status(Base):

	# Define Table Name
	__tablename__ = "Status"

	# Define Columns
	Status_ID = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
	Description = Column(String(255), nullable=False, unique=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=text('now()'))

	# Define Relationships
	devices = relationship("Device", back_populates="status")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_status_description', 'Description'),
	)

# [H] Device Database Model
class Device(Base):

	# Define Table Name
	__tablename__ = "Device"

	# Define Columns
	Device_ID = Column(String(21), primary_key=True, unique=True, nullable=False)
	Status_ID = Column(Integer, ForeignKey("Status.Status_ID"), nullable=False)
	Version_ID = Column(Integer, ForeignKey("Version.Version_ID"), nullable=False)
	Project_ID = Column(Integer, ForeignKey("Project.Project_ID"), nullable=True)
	Model_ID = Column(Integer, ForeignKey("Model.Model_ID"), nullable=False)
	Manufacturer_ID = Column(Integer, ForeignKey("Manufacturer.Manufacturer_ID"), nullable=False)
	IMEI = Column(String(16), ForeignKey("Modem.IMEI"), nullable=False)
	Device_Name = Column(String(100), nullable=True)
	Last_Connection_IP = Column(String(15), nullable=True)
	Last_Connection_Time = Column(TIMESTAMP(timezone=True), nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=text('now()'))
	Description = Column(String(255), nullable=True)

	# Define Relationships
	streams = relationship("Stream", back_populates="device")
	status = relationship("Status", back_populates="devices")
	version = relationship("Version", back_populates="devices")
	project = relationship("Project", back_populates="devices")
	model = relationship("Model", back_populates="devices")
	manufacturer = relationship("Manufacturer", back_populates="devices")
	modem = relationship("Modem", back_populates="devices")
	calibrations = relationship("Calibration", back_populates="device")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_device_id', 'Device_ID'),
		Index('idx_model_id', 'Model_ID'),
		Index('idx_manufacturer_id', 'Manufacturer_ID'),
		Index('idx_status_id', 'Status_ID'),
		Index('idx_device_version_id', 'Version_ID'),
		Index('idx_project_id', 'Project_ID'),
	)

# Project Database Model
class Project(Base):

	# Define Table Name
	__tablename__ = "Project"

	# Define Columns
	Project_ID = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
	Project_Name = Column(String(100), nullable=False, unique=True)
	Project_Description = Column(String(255), nullable=False)
	Status = Column(Boolean, nullable=False, server_default="1")
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=text('now()'))

	# Define Relationships
	devices = relationship("Device", back_populates="project")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_project_name', 'Project_Name'),
	)

# [O] Data_Segment Database Model
class Data_Segment(Base):

	# Define Table Name
	__tablename__ = "Data_Segment"

	# Define Columns
	Segment_ID = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
	Segment_Name = Column(String(100), nullable=False, unique=True)
	Description = Column(String(255), nullable=False)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=text('now()'))

	# Relationship with Variable
	variables = relationship("Variable", back_populates="segment")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_segment_name', 'Segment_Name'),
		Index('idx_segment_description', 'Description'),
	)

# [N] Variable Database Model
class Variable(Base):

	# Define Table Name
	__tablename__ = "Variable"

	# Define Columns
	Variable_ID = Column(String(20), primary_key=True, unique=True, nullable=False)
	Variable_Name = Column(String(100), nullable=False, unique=True) 
	Variable_Description = Column(String(255), nullable=False, unique=True)
	Variable_Unit = Column(String(10), nullable=True)
	Segment_ID = Column(Integer, ForeignKey("Data_Segment.Segment_ID"), nullable=False)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=text('now()'))

	# Define Relationships
	segment = relationship("Data_Segment", back_populates="variables")
	measurements = relationship("Measurement", back_populates="variable")
	calibrations = relationship("Calibration", back_populates="variable")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_variable_id', 'Variable_ID'),
		Index('idx_variable_name', 'Variable_Name'),
		Index('idx_segment_id', 'Segment_ID'),
	)

# [L] Measurement Database Model
class Measurement(Base):

	# Define Table Name
	__tablename__ = "Measurement"

	# Define Columns
	Measurement_ID = Column(Integer, primary_key=True, unique=True, nullable=False)
	Stream_ID = Column(Integer, ForeignKey("Stream.Stream_ID", ondelete="CASCADE"), nullable=False)
	Variable_ID = Column(String(20), ForeignKey("Variable.Variable_ID", ondelete="CASCADE"), nullable=False)
	Measurement_Value = Column(Float, nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

	# Define Relationships
	stream = relationship("Stream", back_populates="measurements")
	variable = relationship("Variable", back_populates="measurements")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_stream_variable', 'Stream_ID', 'Variable_ID'),
		Index('idx_measurement_value', 'Measurement_Value'),
	)

# [J] Stream Database Model
class Stream(Base):

	# Define Table Name
	__tablename__ = "Stream"

	# Define Columns
	Stream_ID = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
	Device_ID = Column(String(21), ForeignKey("Device.Device_ID", ondelete="CASCADE"), nullable=False)
	ICCID = Column(String(21), ForeignKey("SIM.ICCID"), nullable=False)
	Client_IP = Column(String(16), nullable=True)
	Size = Column(Integer, nullable=True)
	RAW_Data = Column(JSON, nullable=True)
	Device_Time = Column(TIMESTAMP(timezone=True), nullable=False)
	Stream_Time = Column(TIMESTAMP(timezone=True), nullable=False)

	# Define Relationships
	device = relationship("Device", back_populates="streams")
	sim = relationship("SIM", back_populates="streams")
	measurements = relationship("Measurement", back_populates="stream")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_stream_device_id', 'Device_ID'),
		Index('idx_stream_iccid', 'ICCID'),
		Index('idx_stream_time', 'Stream_Time'),
		Index('idx_device_time', 'Device_Time'),
	)

# Service_LOG Database Model
class Service_LOG(Base):

	# Define Table Name
	__tablename__ = "Service_LOG"

	# Define Columns
	Service_LOG_ID = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
	Service_Name = Column(String(100), nullable=False, unique=True)
	Service_Status = Column(Boolean, nullable=False, default=False)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=text('now()'))

	# Define Table Arguments
	__table_args__ = (
		Index('idx_service_name', 'Service_Name'),
		Index('idx_update_time', 'Update_Time'),
	)

# Calibration Database Model
class Calibration(Base):

	# Define Table Name
	__tablename__ = "Calibration"

	# Define Columns
	Calibration_ID = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
	Device_ID = Column(String(21), ForeignKey("Device.Device_ID", ondelete="CASCADE"), nullable=False)
	Variable_ID = Column(String(20), ForeignKey("Variable.Variable_ID", ondelete="CASCADE"), nullable=False)
	Gain = Column(Float, nullable=False, server_default="1")
	Offset = Column(Float, nullable=False, server_default="0")
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=text('now()'))

	# Define Relationships
	device = relationship("Device", back_populates="calibrations")
	variable = relationship("Variable", back_populates="calibrations")

	# Define Relationships
	__table_args__ = (
        Index('idx_calibration_device_id', 'Device_ID'),
        Index('idx_calibration_variable_id', 'Variable_ID'),
		UniqueConstraint('Device_ID', 'Variable_ID', name='uix_device_variable'),
	)

# Firmware Database Model
class Firmware(Base):

	# Define Table Name
	__tablename__ = "Firmware"

	# Define Columns
	Firmware_ID = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
	Version_ID = Column(Integer, ForeignKey("Version.Version_ID", ondelete="CASCADE"), nullable=False)
	File_Name = Column(String(255), nullable=True)
	Size = Column(Integer, nullable=True)
	Checksum = Column(String(64), nullable=True)
	Title = Column(String(100), nullable=True)
	URL = Column(String(255), nullable=True)
	Description = Column(String(255), nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=text('now()'))

	# Define Relationships
	version = relationship("Version", back_populates="firmwares")

	# Define Relationships
	__table_args__ = (
    	Index('idx_file_name', 'File_Name'),
    	Index('idx_version_id', 'Version_ID'),
	    Index('idx_create_time', 'Create_Time'),
		UniqueConstraint('File_Name', 'Version_ID', name='uix_file_version'),
	)
