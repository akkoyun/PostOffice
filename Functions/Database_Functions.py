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

	# Log Message
	Log.Terminal_Log("INFO", f"1")

	# Define DB
	with Database.DB_Session_Scope() as DB:

		# Create New Unknown Data
		New_Unknown_Data = Models.Unknown_Data(
			Client_IP = Client_IP,
			RAW_Data = RAW_Data,
			Size = len(RAW_Data)
		)

		# Log Message
		Log.Terminal_Log("INFO", f"2")

		# Add New_Unknown_Data to DataBase
		DB.add(New_Unknown_Data)

		# Commit DataBase
		DB.commit()

		# Refresh DataBase
		DB.refresh(New_Unknown_Data)

		# Log Message
		Log.Terminal_Log("INFO", f"2")

		# Get Data_ID
		Data_ID = New_Unknown_Data.Data_ID

		# Log Message
		Log.Terminal_Log("INFO", f"Unkown Data Recorded: {Data_ID}")
