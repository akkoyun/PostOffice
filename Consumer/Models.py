from sqlalchemy import Column, Integer, String, Boolean, FLOAT
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from Database import Base

# Incoming Buffer Database Model
class Incoming_Buffer(Base):

	# Define Buffer Database
	__tablename__ = "Incoming_Buffer"

	# Define Colomns
	Buffer_ID = Column(Integer, primary_key=True, nullable=False)
	Buffer_Created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	Buffer_Device_ID = Column(String, nullable=True)
	Buffer_Command = Column(String, nullable=True)
	Buffer_Client_IP = Column(String, nullable=True)
	Buffer_Data = Column(String, nullable=True)

# Device Info Database Model
class Device_Info(Base):

	# Define Buffer Database
	__tablename__ = "Device_Info"

	# Define Colomns
	Info_ID = Column(Integer, primary_key=True, nullable=False)
	Created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	Device_Time = Column(TIMESTAMP(timezone=True), nullable=True)
	Device_ID = Column(String, nullable=False)
	Hardware_Version = Column(String, nullable=True)
	Firmware_Version = Column(String, nullable=True)
	Temperature = Column(FLOAT, nullable=False)
	Humidity = Column(FLOAT, nullable=False)
