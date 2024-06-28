# Setup Library
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Library Imports
from Setup import Database, Models, Definitions, Database, Schema
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

            # Try to query the Command
            try:

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

			# Except SQLAlchemy Error
            except SQLAlchemyError as e:

                # Log Error
                Log.Terminal_Log('ERROR', f"Error while processing {Command}: {e}")

                # Return 'Unknown' Command ID
                return Definitions.Command.Unknown.value

    except SQLAlchemyError as e:

        # Log Error
        Log.Terminal_Log('ERROR', f"Database session error: {e}")

        # Return 'Unknown' Command ID
        return Definitions.Command.Unknown.value

# Get or Create Connection Function
def Get_or_Create_Connection(ip: str) -> bool:

	# Check for IP Address
	if ip is None:

		# End Function
		return False

	# Try to open a database session
	try:

		# Define DB
		with Database.SessionLocal() as DB_Module:

			# Control Service
			try:

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
				Log.Terminal_Log('ERROR', f"Error while processing {ip}: {e}")

				# Rollback DataBase
				DB_Module.rollback()

				# Return False
				return False

	# Error Handling
	except SQLAlchemyError as e:

		# Log Error
		Log.Terminal_Log('ERROR', f"Database session error: {e}")

		# Return False
		return False

# Get or Create SIM Function
def Get_or_Create_SIM(iccid: str, mcc: int, mnc: int) -> int:

	# Check for ICCID
	if not iccid:

		# Return 'Unknown' SIM ID
		return 1

	# Try to open a database session
	try:

		with Database.SessionLocal() as DB_Module:

			# Try to query the Command
			try:

				# Query ICCID
				SIM_Query = (DB_Module.query(Models.SIM).filter(
					Models.SIM.ICCID.like(iccid)
				).first())

				# SIM Found
				if SIM_Query is not None:

					# Get existing SIM ID
					return SIM_Query.SIM_ID

				# SIM Not Found
				else:

					# Check for MCC and MNC
					if mcc is None or mnc is None:
						mcc = 286
						mnc = 1

					# Check for Operator_ID
					Operator_Query = (DB_Module.query(Models.GSM_Operator).filter(
						Models.GSM_Operator.MCC_ID == mcc,
						Models.GSM_Operator.MNC_ID == mnc
					).first())

					# Operator Found
					if Operator_Query is not None:

						# Get Operator ID
						Operator_ID = Operator_Query.Operator_ID

					# Create New SIM
					New_SIM = Models.SIM(
						ICCID = iccid,
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

			# Except SQLAlchemy Error
			except SQLAlchemyError as e:

				# Log Error
				Log.Terminal_Log('ERROR', f"Error while processing {iccid}: {e}")

				# Return 'Unknown' SIM ID
				return 1

	# Except SQLAlchemy Error
	except SQLAlchemyError as e:

		# Log Error
		Log.Terminal_Log('ERROR', f"Database session error: {e}")

		# Return 'Unknown' SIM ID
		return 1

# Get or Create Firmware Function
def Get_or_Create_Firmware(firmware: str) -> int:

	# Check for Firmware
	if not firmware:

		# Return 'Unknown' Firmware ID
		return 0

	# Try to open a database session
	try:

		# Define DB
		with Database.SessionLocal() as DB_Module:

			# Try to query the Command
			try:

				# Query Firmware
				Firmware_Query = (DB_Module.query(Models.Version).filter(
					Models.Version.Firmware.like(firmware)
				).first())

				# Check if Firmware exists
				if Firmware_Query is not None:

					# Get existing Firmware ID
					return Firmware_Query.Version_ID
				
				# Firmware Not Found
				else:

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
					return New_Firmware.Version_ID
			
			# Except SQLAlchemy Error
			except SQLAlchemyError as e:

				# Log Error
				Log.Terminal_Log('ERROR', f"Error while processing {firmware}: {e}")

				# Return 'Unknown' Firmware ID
				return 0
	
	# Except SQLAlchemy Error
	except SQLAlchemyError as e:

		# Log Error
		Log.Terminal_Log('ERROR', f"Database session error: {e}")

		# Return 'Unknown' Firmware ID
		return 0

# Get or Create Modem Function
def Get_or_Create_Modem(imei: str) -> bool:

	# Check for IMEI
	if not imei:

		# Return 'Unknown' Modem
		return False

	# Try to open a database session
	try:

		# Define DB
		with Database.SessionLocal() as DB_Module:

			# Try to query the Command
			try:

				# Query Modem
				Modem_Query = (DB_Module.query(Models.Modem).filter(
					Models.Modem.IMEI.like(imei)
				).first())

				# Check if Modem exists
				if Modem_Query is not None:

					# Get existing Modem ID
					return False
				
				# Modem Not Found
				else:

					# Create New Modem
					New_Modem = Models.Modem(
						IMEI = imei,
						Model_ID = 0,
						Manufacturer_ID = 0
					)

					# Add Modem to DataBase
					DB_Module.add(New_Modem)

					# Commit DataBase
					DB_Module.commit()

					# Refresh DataBase
					DB_Module.refresh(New_Modem)

					# Return New Modem
					return True

			# Except SQLAlchemy Error
			except SQLAlchemyError as e:

				# Log Error
				Log.Terminal_Log('ERROR', f"Error while processing {imei}: {e}")

				# Return 'Unknown' Modem
				return False

	# Except SQLAlchemy Error
	except SQLAlchemyError as e:

		# Log Error
		Log.Terminal_Log('ERROR', f"Database session error: {e}")

		# Return 'Unknown' Modem
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


