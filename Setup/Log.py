# Library Includes
from .Config import APP_Settings
import logging, coloredlogs
from . import Database, Models, Log

# Set Log Options
Service_Logger = logging.getLogger(__name__)
logging.basicConfig(filename=APP_Settings.POSTOFFICE_LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

# Set Log Colored
coloredlogs.install(level='DEBUG', logger=Service_Logger)

# Start Log Message
def Start_Log():
    
	# Log Message
	Service_Logger.debug("Service Started.")

# Stop Log Message
def Stop_Log():
    
	# Log Message
	Service_Logger.debug("Service Stopped.")

# WeatherStat Log Message
def WeatherStat_Log(ID, Company, Device, Command):

    # Log Message
    Service_Logger.info(f"['{ID}'] - Incomming data pack from ['{Company}'] - ['{Device}'] with ['{Command}']")

# WebSocket Log Message
def WebSocket_Data_Log(ID, Command, Direction):

    # Log Message
	if Direction == "Out":
		Service_Logger.info(f"['{ID}'] - Outgoing WebSocket data. ['{Command}']")
	elif Direction == "In":
		Service_Logger.info(f"['{ID}'] - Incomming WebSocket data. ['{Command}']")

	# Create Add Record Command
	New_Log = Models.WebSocket_Log(
		Log_Device_ID = ID,
		Log_Direction = Direction,
		Log_Command = Command)

	# Define DB
	DB_Log = Database.SessionLocal()

	# Add and Refresh DataBase
	DB_Log.add(New_Log)
	DB_Log.commit()
	DB_Log.refresh(New_Log)

	# Close Database
	DB_Log.close()







# Unknown Log Message
def Unknown_Log(request):

	Service_Logger.error(f"Unknown data come from device. ['{request.client.host}']")

# Wrong Device Log Message
def Wrong_Device_Log(Company, Device, Command):

	Service_Logger.error(f"Wrong device data pack from ['{Company}'] - ['{Device}'] (WeatherStat) with ['{Command}']")

# Status TimeStamp Log Message
def Status_TimeStamp_Log(request):

	# Log Message
	Service_Logger.info(f"Status check from ['{request.client.host}']")

# Status Unknown Log Message
def Status_Unknown_Log(request):

	# Log Message
    Service_Logger.error(f"Bad status check from ['{request.client.host}']")

# Get Request Log Message
def Get_Log(request):

	# Log Message
	Service_Logger.debug(f"Incomming GET request from ['{request.client.host}']")