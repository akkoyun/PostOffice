# Setup Library
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Library Imports
from Setup import Database, Models, Definitions, Schema
from Functions import Log
from pydantic import Field
from sqlalchemy.exc import SQLAlchemyError
import pytz, time
from typing import Optional

# Set Timezone
Local_Timezone = pytz.timezone("Europe/Istanbul")

# Record Unkown Data
def Record_Unknown_Data(Client_IP: str, RAW_Data: str):

	try:

		# Define DB
		with Database.DB_Session_Scope() as DB:

			# Create New Unknown Data
			New_Unknown_Data = Models.Unknown_Data(
				Client_IP = Client_IP,
				RAW_Data = RAW_Data,
				Size = len(RAW_Data)
			)

			try:

				# Add New_Unknown_Data to DataBase
				DB.add(New_Unknown_Data)

				# Commit DataBase
				DB.commit()

				# Refresh DataBase
				DB.refresh(New_Unknown_Data)

			except Exception as e:

				# Log Message
				Log.Terminal_Log("ERROR", f"Database operation failed: {str(e)}")

				# Rollback DataBase
				raise

			# Get Data_ID
			Data_ID = New_Unknown_Data.Data_ID

			# Log Message
			Log.Terminal_Log("INFO", f"Unknown Data Recorded: {Data_ID}")

	except Exception as e:

		# Log Message
		Log.Terminal_Log("ERROR", f"An error occurred: {str(e)}")

# Get or Create Connection Function
def Get_or_Create_Connection(ip: str) -> bool:

	# Check for IP Address
	if not ip:

		# End Function
		return False

	# Try to open a database session
	try:

		# Define DB
		with Database.SessionLocal() as DB_Module:

			# Query IP Address
			IP_Query = (DB_Module.query(Models.Connection).filter(
				Models.Connection.IP_Address.like(ip)
			).first())

			# IP Address Found
			if IP_Query is not None:

				# Update Connection
				IP_Query.Update_Time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

				# Commit DataBase
				DB_Module.commit()

				# Return Existed Connection
				return False

			# IP Address Not Found
			else:

				# Create New Connection
				New_IP = Models.Connection(
					IP_Address = ip,
					IP_Pool = 0,
					Update_Time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
				)

				# Add Connection to DataBase
				DB_Module.add(New_IP)

				# Commit DataBase
				DB_Module.commit()

				# Refresh DataBase
				DB_Module.refresh(New_IP)

				# Return New Connection
				return True

	# Error Handling
	except SQLAlchemyError as e:

		# Log Error
		Log.Terminal_Log('ERROR', f"Database session error: {e}")

		# Rollback DataBase
		DB_Module.rollback()

		# Return False
		return False

# Get or Create Device Function
def Get_or_Create_Device(id: str, firmware: int, imei: str, ip: str, time: str) -> bool:

	# Check for Parameters
	if not id or not firmware or not imei or not ip or not time:

		# Return 'Unknown' Modem
		return False

	# Try to open a database session
	try:

		# Define DB
		with Database.SessionLocal() as DB_Module:

			# Try to query the Command
			try:

				# Query Device
				Device_Query = (DB_Module.query(Models.Device).filter(
					Models.Device.Device_ID.like(id)
				).first())

				# Device Not Found
				if Device_Query is None:

					# Create New Device
					New_Device = Models.Device(
						Device_ID = id,
						Status_ID = 0,
						Version_ID = firmware,
						Project_ID = 0,
						Model_ID = 0,
						Manufacturer_ID = 0, 
						IMEI = imei,
						Last_Connection_IP = ip,
						Last_Connection_Time = time,
					)

					# Add Device to DataBase
					DB_Module.add(New_Device)

					# Commit DataBase
					DB_Module.commit()

					# Refresh DataBase
					DB_Module.refresh(New_Device)

					# Return New Device
					return True
				
				# Device Found
				else:

					# Update Device
					Device_Query.Version_ID = firmware
					Device_Query.Last_Connection_IP = ip
					Device_Query.Last_Connection_Time = time

					# Commit DataBase
					DB_Module.commit()

					# Return Existed Device
					return False

			# Except SQLAlchemy Error
			except SQLAlchemyError as e:

				# Log Error
				Log.Terminal_Log('ERROR', f"Error while processing {id}: {e}")

				# Return 'Unknown' Modem
				return False
	
	# Except SQLAlchemy Error
	except SQLAlchemyError as e:

		# Log Error
		Log.Terminal_Log('ERROR', f"Database session error: {e}")

		# Return 'Unknown' Modem
		return False

# Create Stream Function
def Create_Stream(Stream_Data: dict, Headers: dict) -> int:

	# Try to open a database session
	try:

		# Define DB
		with Database.SessionLocal() as DB_Module:

			# Try to query the Command
			try:

				# Create New Stream
				New_Stream = Models.Stream(
					Device_ID = Stream_Data.message.Info.ID,
					Command_ID = Stream_Data.command_id,
					SIM_ID = Stream_Data.sim_id,
					IP_Address = Headers['Device_IP'],
					Size = Headers['Size'],
					Device_Time = Headers['Device_Time'],
					Stream_Time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
				)

				# Add Stream to DataBase
				DB_Module.add(New_Stream)

				# Commit DataBase
				DB_Module.commit()

				# Refresh DataBase
				DB_Module.refresh(New_Stream)

				# Get Stream ID
				return New_Stream.Stream_ID
			
			# Except SQLAlchemy Error
			except SQLAlchemyError as e:

				# Log Error
				Log.Terminal_Log('ERROR', f"Error while processing {Stream_Data.message.Info.ID}: {e}")

				# Return 'Unknown' Stream ID
				return 0
	
	# Except SQLAlchemy Error
	except SQLAlchemyError as e:

		# Log Error
		Log.Terminal_Log('ERROR', f"Database session error: {e}")

		# Return 'Unknown' Stream ID
		return 0

# Record Measurements Function
def Record_Measurement(Pack, Stream: int, Segment: int) -> int:

	# Define Record Count
	New_Record_Count = 0

	# Define DB
	DB_Module = Database.SessionLocal()

	# Get Pack Dictionary
	try:

		# Query all data types
		Data_Type_Query = DB_Module.query(Models.Variable).filter(Models.Variable.Segment_ID == Segment).all()

		# Get Data Type List
		Formatted_Data = [(Variable.Variable_ID, Variable.Variable_Unit) for Variable in Data_Type_Query]

	finally:
		
		# Close Database
		DB_Module.close()

	# Define Found Variables
	Found_Variables = {}

	# Check for Tuple and Extract Variable IDs
	keys_to_check = [var[0] if isinstance(var, tuple) else var for var in Formatted_Data]

	# Get Pack Dictionary
	Pack_Dict = Pack.__dict__

	# Check for Variables
	for variable in keys_to_check:

		# Check for Variable
		if variable in Pack_Dict:

			# Get Value
			value = Pack_Dict[variable]

			# Check for Value
			if value is not None and value != "":

				# Add to Found Variables
				Found_Variables[variable] = value

	# Record Measurements
	try:

		# Define DB
		with Database.SessionLocal() as DB_Module:

			# Log Variables
			for Variable, Value in Found_Variables.items():

				# Record Measurement
				try:

					# New Measurement
					New_Measurement = Models.Measurement(
						Stream_ID=Stream,
						Variable_ID=Variable,
						Measurement_Value=Value
					)

					# Add Stream to DataBase
					DB_Module.add(New_Measurement)

					# Commit DataBase
					DB_Module.commit()

					# Refresh DataBase
					DB_Module.refresh(New_Measurement)

					# Update Record Count
					New_Record_Count += 1

				except SQLAlchemyError as e:

					# Rollback in case of error
					DB_Module.rollback()

					# Log Error
					Log.Terminal_Log('ERROR', f"Error while processing {Variable}: {e}")

					# Return 'Unknown' Stream ID
					return 0

		# End Function
		return New_Record_Count

	# Error Handling
	except SQLAlchemyError as e:

		# Log Error
		Log.Terminal_Log('ERROR', f"Database session error: {e}")

		# Return 'Unknown' Stream ID
		return 0

# Dynamic Model Creator
def Create_Dynamic_Model(Segment_ID: int = 0):

	# Define Variables List
	Felds = {}
	Annotations = {}

	# Try to open a database session
	try:

		# Open a database session
		with Database.DB_Session_Scope() as DB:

			# Query all data types
			if Segment_ID == 0:
				Query_Variables = DB.query(Models.Variable).filter(
					Models.Variable.Segment_ID.in_([1, 4, 5, 6, 7, 8, 9])
				).all()
			else:
				Query_Variables = DB.query(Models.Variable).filter(
					Models.Variable.Segment_ID == Segment_ID
				).all()

			# Get Data Type List
			for Variable in Query_Variables:

				# Field definition
				field_info = Field(
					default=None, 
					description=Variable.Variable_Description,
					ge=Variable.Variable_Min_Value if Variable.Variable_Min_Value is not None else None,
					le=Variable.Variable_Max_Value if Variable.Variable_Max_Value is not None else None
				)

				# Assign Field and Type annotations
				Felds[Variable.Variable_ID] = field_info
				Annotations[Variable.Variable_ID] = Optional[float]

		# Create Dynamic Model with type and annotations
		return type('DynamicModel', (Schema.CustomBaseModel,), {'__annotations__': Annotations, **Felds})

	# Handle Exceptions
	except SQLAlchemyError as e:

		# Raise Error
		raise RuntimeError(f"Failed to create dynamic model due to database error: {str(e)}") from e

	# Handle Exceptions
	except Exception as e:

		# Raise Error
		raise RuntimeError(f"An unexpected error occurred while creating the dynamic model: {str(e)}") from e

# Increase Rule Trigger Count
def Increase_Rule_Trigger_Count(Rule_ID: int) -> int:

	# Try to open a database session
	try:

		# Open a database session
		with Database.DB_Session_Scope() as DB:

			# Query Rule
			Rule_Update = DB.query(Models.Rules).filter(
				Models.Rules.Rule_ID == Rule_ID
			).first()

			# Rule Not Found
			if Rule_Update is None:

				# Log Error
				Log.Terminal_Log('ERROR', f"Rule ID: {Rule_ID} not found")

				# Return Rule ID
				return 0
			
			# Update Rule
			else:

				# Update Rule
				Rule_Update.Rule_Trigger_Count += 1

				# Commit Update
				DB.commit()

				# Return Rule ID
				return Rule_ID

	# Handle Exceptions
	except SQLAlchemyError as e:

		# Log Error
		Log.Terminal_Log('ERROR', f"Error while processing Rule ID: {Rule_ID}: {e}")

		# Return Rule ID
		return 0

# Get All Variables
def Get_All_Variables():

	# Try to open a database session
	try:

		# Open a database session
		with Database.DB_Session_Scope() as DB:

			# Query all data types
			Query_Variables = DB.query(Models.Variable).all()

			# Get Data Type List
			return [(Variable.Variable_ID, Variable.Variable_Unit) for Variable in Query_Variables]

	# Handle Exceptions
	except SQLAlchemyError as e:

		# Log Error
		Log.Terminal_Log('ERROR', f"Error while Variable Get: {e}")

		# Return Empty Dictionary
		return {}














# Get Command ID Function
def Get_Command_ID(Command: str) -> int:

	# Check for Command
	if not Command:

		# Return 'Unknown' Command ID
		return Definitions.Command.Unknown.value

	# Try to open a database session
	try:

		# Define DB
		with Database.SessionLocal() as DB_Module:

			# Query Command
			Command_Query = DB_Module.query(Models.Command).filter(
				Models.Command.Command.like(Command)
			).first()

			# Check if Command exists
			if Command_Query is not None:

				# Get existing Command ID
				return Command_Query.Command_ID
				
			# Command Not Found
			else:

				# Return 'Unknown' Command ID
				return Definitions.Command.Unknown.value

	# Error Handling
	except SQLAlchemyError as e:

		# Log Error
		Log.Terminal_Log('ERROR', f"Database session error: {e}")

		# Rollback DataBase
		DB_Module.rollback()

		# Return 'Unknown' Command ID
		return Definitions.Command.Unknown.value

# Get Operator ID Function
def Get_Operator_ID(MCC: int, MNC: int) -> int:

	# Set Default MCC
	if MCC is None:
		MCC = Definitions.GSM_Operator.Default_MCC.value
	
	# Set Default MNC
	if MNC is None:
		MNC = Definitions.GSM_Operator.Default_MNC.value

	# Try to open a database session
	try:

		# Define DB
		with Database.SessionLocal() as DB_Module:

			# Query Operator
			Operator_Query = (DB_Module.query(Models.GSM_Operator).filter(
				Models.GSM_Operator.MCC_ID == MCC,
				Models.GSM_Operator.MNC_ID == MNC
			).first())

			# Check if Operator exists
			if Operator_Query is not None:

				# Get existing Operator ID
				return Operator_Query.Operator_ID
			
			# Operator Not Found
			else:

				# Return 'Unknown' Operator ID
				return Definitions.GSM_Operator.Unknown.value

	# Error Handling
	except SQLAlchemyError as e:

		# Log Error
		Log.Terminal_Log('ERROR', f"Database session error: {e}")

		# Return 'Unknown' Operator ID
		return Definitions.GSM_Operator.Unknown.value

# Create New SIM Function
def Create_New_SIM(ICCID: str, Operator_ID: int) -> int:

	# Try to open a database session
	try:

		# Define DB
		with Database.SessionLocal() as DB_Module:

			# Create New SIM
			New_SIM = Models.SIM(
				ICCID = ICCID,
				Operator_ID = Operator_ID
			)

			# Add SIM to DataBase
			DB_Module.add(New_SIM)

			# Commit DataBase
			DB_Module.commit()

			# Refresh DataBase
			DB_Module.refresh(New_SIM)

			# Return New SIM
			return New_SIM.SIM_ID

	# Error Handling
	except SQLAlchemyError as e:

		# Log Error
		Log.Terminal_Log('ERROR', f"Database session error: {e}")

		# Return 'Unknown' SIM ID
		return Definitions.SIM.Unknown.value

# Get SIM ID Function
def Get_SIM_ID(ICCID: str) -> int:

	# Check for ICCID
	if not ICCID:

		# Return 'Unknown' SIM ID
		return Definitions.SIM.Unknown.value

	# Try to open a database session
	try:

		# Define DB
		with Database.SessionLocal() as DB_Module:

			# Query ICCID
			SIM_Query = (DB_Module.query(Models.SIM).filter(
				Models.SIM.ICCID.like(ICCID)
			).first())

			# SIM Found
			if SIM_Query is not None:

				# Get existing SIM ID
				return SIM_Query.SIM_ID

			# SIM Not Found
			else:

				# Return 'Unknown' SIM ID
				return Definitions.SIM.Unknown.value

	# Except SQLAlchemy Error
	except SQLAlchemyError as e:

		# Log Error
		Log.Terminal_Log('ERROR', f"Database session error: {e}")

		# Return 'Unknown' SIM ID
		return Definitions.SIM.Unknown.value

# Get or Create SIM Function
def Get_or_Create_SIM(iccid: str, mcc: int, mnc: int) -> int:

	# Get SIM ID
	SIM_ID = Get_SIM_ID(iccid)

	# SIM Found
	if SIM_ID != Definitions.SIM.Unknown.value:

		# Return Existing SIM ID
		return SIM_ID
	
	# SIM Not Found
	else:

		# Get Operator ID
		Operator_ID = Get_Operator_ID(mcc, mnc)

		# Record New SIM
		New_SIM_ID = Create_New_SIM(iccid, Operator_ID)

		# Return New SIM ID
		return New_SIM_ID

# Get Firmware ID Function
def Get_Firmware_ID(Firmware: str) -> int:

	# Check for Firmware
	if not Firmware:

		# Return 'Unknown' Firmware ID
		return Definitions.Firmware.Unknown.value

	# Try to open a database session
	try:

		# Define DB
		with Database.SessionLocal() as DB_Module:

			# Query Firmware
			Firmware_Query = (DB_Module.query(Models.Version).filter(
				Models.Version.Firmware.like(Firmware)
			).first())

			# Check if Firmware exists
			if Firmware_Query is not None:

				# Get existing Firmware ID
				return Firmware_Query.Version_ID
			
			# Firmware Not Found
			else:

				# Return 'Unknown' Firmware ID
				return Definitions.Firmware.Unknown.value

	# Error Handling
	except SQLAlchemyError as e:

		# Log Error
		Log.Terminal_Log('ERROR', f"Database session error: {e}")

		# Return 'Unknown' Firmware ID
		return Definitions.Firmware.Unknown.value

# Create Firmware Function
def Create_Firmware(firmware: str) -> int:

	# Try to open a database session
	try:

		# Define DB
		with Database.SessionLocal() as DB_Module:

			# Create New Firmware
			New_Firmware = Models.Version(
				Firmware = firmware
			)

			# Add Firmware to DataBase
			DB_Module.add(New_Firmware)

			# Commit DataBase
			DB_Module.commit()

			# Refresh DataBase
			DB_Module.refresh(New_Firmware)

			# Return New Firmware
			return New_Firmware.Firmware_ID

	# Error Handling
	except SQLAlchemyError as e:

		# Log Error
		Log.Terminal_Log('ERROR', f"Database session error: {e}")

		# Return 'Unknown' Firmware ID
		return Definitions.Firmware.Unknown.value

# Get or Create Firmware Function
def Get_or_Create_Firmware(firmware: str) -> int:

	# Get Firmware ID
	Firmware_ID = Get_Firmware_ID(firmware)

	# Firmware Found
	if Firmware_ID != Definitions.Firmware.Unknown.value:

		# Return Existing Firmware ID
		return Firmware_ID
	
	# Firmware Not Found
	else:

		# Create New Firmware
		New_Firmware_ID = Create_Firmware(firmware)

		# Return New Firmware ID
		return New_Firmware_ID

# Control Modem Function
def Control_Modem(IMEI: str) -> bool:

	# Check for IMEI
	if not IMEI:

		# Return False
		return False

	# Try to open a database session
	try:

		# Define DB
		with Database.SessionLocal() as DB_Module:

			# Query Modem
			Modem_Query = (DB_Module.query(Models.Modem).filter(
				Models.Modem.IMEI.like(IMEI)
			).first())

			# Check if Modem exists
			if Modem_Query is not None:

				# Return True
				return True
			
			# Modem Not Found
			else:

				# Return False
				return False

	# Error Handling
	except SQLAlchemyError as e:

		# Log Error
		Log.Terminal_Log('ERROR', f"Database session error: {e}")

		# Return False
		return False

# Create New Modem Function
def Create_New_Modem(IMEI: str, Model: int, Manufacturer: int) -> bool:

	# Check for Model
	if Model is None:
		Model = 0

	# Check for Manufacturer
	if Manufacturer is None:
		Manufacturer = 0

	# Check for IMEI
	if not IMEI:
		return False

	# Try to open a database session
	try:

		# Define DB
		with Database.SessionLocal() as DB_Module:

			# Create New Modem
			New_Modem = Models.Modem(
				IMEI = IMEI,
				Model_ID = Model,
				Manufacturer_ID = Manufacturer
			)

			# Add Modem to DataBase
			DB_Module.add(New_Modem)

			# Commit DataBase
			DB_Module.commit()

			# Refresh DataBase
			DB_Module.refresh(New_Modem)

			# Return New Modem
			return True

	# Error Handling
	except SQLAlchemyError as e:

		# Log Error
		Log.Terminal_Log('ERROR', f"Database session error: {e}")

		# Rollback DataBase
		DB_Module.rollback()

		# Return 'Unknown' Modem ID
		return False

# Get or Create Modem Function
def Get_or_Create_Modem(imei: str) -> bool:

	# Control Modem
	Modem_Control = Control_Modem(imei)

	# Modem Found
	if Modem_Control:

		# Return Existing Modem
		return True
	
	# Modem Not Found
	else:

		# Create New Modem
		New_Modem = Create_New_Modem(imei, 0, 0)

		# Return New Modem
		return New_Modem

# Control Device Function
def Control_Device(ID: str, Version_ID: int, IP: str, Connection_Time: str) -> bool:

	# Check for ID
	if not ID:

		# Return False
		return False

	# Check for Version ID
	if Version_ID is None:
		Version_ID = Definitions.Firmware.Unknown.value

	# Check for IP
	if not IP:
		IP = "0.0.0.0"

	# Check for Connection Time
	if not Connection_Time:
		Connection_Time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

	# Try to open a database session
	try:

		# Define DB
		with Database.SessionLocal() as DB_Module:

			# Query Device
			Device_Query = (DB_Module.query(Models.Device).filter(
				Models.Device.Device_ID.like(ID)
			).first())

			# Check if Device exists
			if Device_Query is not None:

				# Update Device
				Device_Query.Last_Connection_IP = IP
				Device_Query.Last_Connection_Time = Connection_Time
				Device_Query.Version_ID = Version_ID

				# Return True
				return True
			
			# Device Not Found
			else:

				# Return False
				return False

	# Error Handling
	except SQLAlchemyError as e:

		# Log Error
		Log.Terminal_Log('ERROR', f"Database session error: {e}")

		# Return False
		return False



	







# Add Rule Log
def Add_Rule_Log(Rule_ID: int, Device_ID: int) -> int:

	# Try to open a database session
	try:

		# Open a database session
		with Database.DB_Session_Scope() as DB:

			# Create New Rule Log
			New_Rule_Log = Models.Rule_Log(
				Device_ID = Device_ID,
				Rule_ID = Rule_ID
			)

			# Add Rule Log to DataBase
			DB.add(New_Rule_Log)

			# Commit DataBase
			DB.commit()

			# Refresh DataBase
			DB.refresh(New_Rule_Log)

			# Return Rule Log ID
			return New_Rule_Log.Rule_Log_ID

	# Handle Exceptions
	except SQLAlchemyError as e:

		# Log Error
		Log.Terminal_Log('ERROR', f"Error while processing Rule ID: {Rule_ID}: {e}")

		# Return Rule Log ID
		return 0












# Handle Packet Function
def Handle_Packet(Device_ID: str, Packet: dict) -> dict:

	# Ensure Packet is a dictionary
	if not isinstance(Packet, dict):
		raise ValueError("Packet must be a dictionary")

	# Get All Variables
	Formatted_Data = Get_All_Variables()

	# Define Found Variables
	Found_Variables = {}

	# Check for Tuple and Extract Variable IDs
	Keys_To_Check = [var[0] if isinstance(var, tuple) else var for var in Formatted_Data]

	# Get Data Packs
	Device_Pack = Packet.get('Device', {})
	Power_Pack = Device_Pack.get('Power', {})
	IoT_Pack = Device_Pack.get('IoT', {})
	Payload_Pack = Packet.get('Payload', {})

	# Add Device ID to Found Variables
	Found_Variables['Device_ID'] = Device_ID

	# Function To Check Variables in a Given Pack
	def Check_Variables_in_Pack(pack, pack_name):

		# Check for Variables
		for variable in Keys_To_Check:

			# Check for Variable
			if variable in pack:

				# Get Value
				value = pack[variable]

				# Check for Value
				if value is not None and value != "":

					# Add to Found Variables
					Found_Variables[variable] = value

	# Check Variables in Packs
	Check_Variables_in_Pack(Power_Pack, 'Power_Pack')
	Check_Variables_in_Pack(IoT_Pack, 'IoT_Pack')
	Check_Variables_in_Pack(Payload_Pack, 'Payload')

	# Return Found Variables
	return Found_Variables

