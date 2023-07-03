from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .Database import Base, SessionLocal, DB_Engine

# Incoming Buffer Database Model
class Wrong_Data_Buffer(Base):

	# Define Buffer Database
	__tablename__ = "Wrong_Data_Buffer"

	# Define Colomns
	Buffer_ID = Column(Integer, primary_key=True, nullable=False)
	Buffer_Created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	Buffer_Client_IP = Column(String, nullable=True)
	Buffer_Data = Column(String, nullable=True)

# Incoming Buffer Database Model
class Valid_Data_Buffer(Base):

	# Define Buffer Database
	__tablename__ = "Valid_Data_Buffer"

	# Define Colomns
	Buffer_ID = Column(Integer, primary_key=True, nullable=False)
	Buffer_Created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	Buffer_Device_ID = Column(String, nullable=True)
	Buffer_Company = Column(String, nullable=True)
	Buffer_Device = Column(String, nullable=True)
	Buffer_Command = Column(String, nullable=True)
	Buffer_Client_IP = Column(String, nullable=True)
	Buffer_Data = Column(String, nullable=True)
	Parse_Device = Column(Boolean, default=False)
	Parse_Payload = Column(Boolean, default=False)

# WebSocket Log Database Model
class WebSocket_Log(Base):

	# Define Buffer Database
	__tablename__ = "WebSocket_Log"

	# Define Colomns
	Log_ID = Column(Integer, primary_key=True, nullable=False)
	Log_Created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	Log_Device_ID = Column(String, nullable=True)
	Log_Direction = Column(String, nullable=True)
	Log_Command = Column(String, nullable=True)
