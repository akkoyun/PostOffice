# Setup Library
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Library Imports
from Setup import Database, Models
from Functions import Log
import pytz
import time

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
def Get_Command_ID(Command: str):

	# Check for Command
	if Command is not None:

		# Check for Command Table
		try:

			# Define DB
			DB_Module = Database.SessionLocal()

			# Control Service
			Command_Query = (DB_Module.query(Models.Command).filter(
				Models.Command.Command.like(Command)
			).first())

			# Command Found
			if Command_Query is not None:

				# Get Existed Command ID
				Command_ID = Command_Query.Command_ID

				# Return Command ID
				return Command_ID

			else:

				# Return 'Unknown' Command ID
				return 1

		finally:

			# Close Database
			DB_Module.close()

	else :

		# Return 'Unknown' Command ID
		return 1

# Get or Create SIM Function
def Get_or_Create_SIM(iccid: str):

	# Check for ICCID
	if iccid is not None:

		# Check for SIM Table
		try:

			# Define DB
			DB_Module = Database.SessionLocal()

			# Control Service
			SIM_Query = (DB_Module.query(Models.SIM).filter(
				Models.SIM.ICCID.like(iccid)
			).first())

			# SIM Found
			if SIM_Query is None:

				# Create New SIM
				New_SIM = Models.SIM(
					ICCID = iccid,
					Operator_ID = 1 # Daha sonra düzeltilecek şu an manuel olarak yazıldı
				)

				# Add SIM to DataBase
				DB_Module.add(New_SIM)

				# Commit DataBase
				DB_Module.commit()

				# Refresh DataBase
				DB_Module.refresh(New_SIM)
				
				# Return New SIM
				return True
			
			else:

				# Return Existed SIM
				return False

		finally:

			# Close Database
			DB_Module.close()

	else :

		# Return 'Unknown' SIM
		return False

# Get or Create Firmware Function
def Get_or_Create_Firmware(firmware: str):

	# Check for Firmware
	if firmware is not None:

		# Check for Firmware Table
		try:

			# Define DB
			DB_Module = Database.SessionLocal()

			# Control Service
			Firmware_Query = (DB_Module.query(Models.Version).filter(
				Models.Version.Firmware.like(firmware)
			).first())

			# Firmware Found
			if Firmware_Query is None:

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

			else:

				# Return Existed Firmware
				return Firmware_Query.Version_ID

		finally:

			# Close Database
			DB_Module.close()
	
	else:

		# Return 'Unknown' Firmware
		return 0

# Get or Create Modem Function
def Get_or_Create_Modem(imei: str, firmware: str):

	# Check for IMEI
	if imei is not None:

		# Check for Modem Table
		try:

			# Define DB
			DB_Module = Database.SessionLocal()

			# Control Service
			Modem_Query = (DB_Module.query(Models.Modem).filter(
				Models.Modem.IMEI.like(imei)
			).first())

			# Modem Found
			if Modem_Query is None:

				# Create New Modem
				New_Modem = Models.Modem(
					IMEI = imei,
					Model_ID = 0,
					Manufacturer_ID = 0,
					Firmware = firmware,
				)

				# Add Modem to DataBase
				DB_Module.add(New_Modem)

				# Commit DataBase
				DB_Module.commit()

				# Refresh DataBase
				DB_Module.refresh(New_Modem)

				# Return New Modem
				return True

			else:

				# Check for Firmware
				if firmware is not None:

					# Check for Firmware Update
					if Modem_Query.Firmware != firmware:

						# Update Device Firmware
						Modem_Query.Firmware = firmware

						# Commit DataBase
						DB_Module.commit()

				# Return Existed Modem
				return False

		finally:

			# Close Database
			DB_Module.close()

	else:

		# Return 'Unknown' Modem
		return False

# Get or Create Device Function
def Get_or_Create_Device(id: str, firmware: int, imei: str, ip: str, time: str):

	# Check for Device ID
	if id is not None:

		# Check for Device Table
		try:

			# Define DB
			DB_Module = Database.SessionLocal()

			# Control Service
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

		finally:

			# Close Database
			DB_Module.close()

	else:

		# Return 'Unknown' Modem
		return False

# Get or Create Connection Function
def Get_or_Create_Connection(ip: str):

	# Check for IP Address
	if ip is not None:

		# Check for Connection Table
		try:

			# Define DB
			DB_Module = Database.SessionLocal()

			# Control Service
			Connection_Query = (DB_Module.query(Models.Connection).filter(
				Models.Connection.IP_Address.like(ip)
			).first())

			# Connection Found
			if Connection_Query is None:

				# Create New Connection
				New_Connection = Models.Connection(
					IP_Address = ip,
					IP_Pool = 0,
				)

				# Add Connection to DataBase
				DB_Module.add(New_Connection)

				# Commit DataBase
				DB_Module.commit()

				# Refresh DataBase
				DB_Module.refresh(New_Connection)

				# Return New Connection
				return True

			else:

				# Update Connection
				Connection_Query.Update_Time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

				# Commit DataBase
				DB_Module.commit()

				# Return Existed Connection
				return False

		finally:

			# Close Database
			DB_Module.close()

	else:

		# Return 'Unknown' Connection
		return False

# Create Stream Function
def Create_Stream(Stream_Data: dict, Headers: dict):

	# Define DB
	DB_Module = Database.SessionLocal()

	# Record Stream
	New_Stream = Models.Stream(
		Device_ID = Stream_Data.message.Info.ID,
		Command_ID = Stream_Data.command_id,
		ICCID = Stream_Data.iccid,
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




# Get Variables in JSON Function
def Get_Variables(Pack, Segment: int):

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

	# Check for Tuple
	keys_to_check = [var[0] if isinstance(var, tuple) else var for var in Formatted_Data]
	
	# Get Pack Dictionary
	Pack_Dict = Pack.__dict__

	# Check for Variables
	for variable in keys_to_check:

		# Check if variable in Pack_Dict
		if variable in Pack_Dict:

			# Add to Found Variables
			Found_Variables[variable] = Pack_Dict[variable]

	# Return dictionary of Present Variables and their values
	return Found_Variables






