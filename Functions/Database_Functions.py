# Setup Library
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Library Imports
from Setup import Database, Models
from Functions import Log
import pytz

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




