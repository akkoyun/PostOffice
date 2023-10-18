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
    Service_Logger.info(f"['{ID}'] - Incomming data pack ['{Company}'] - ['{Device}'] with ['{Command}']")

# Wrong Device Log Message
def Wrong_Device_Log(Company, Device, Command):

	Service_Logger.error(f"Wrong device data pack ['{Company}'] - ['{Device}'] with ['{Command}']")

# Kafka Device Handle Log Message
def Device_Handler_Log(ID):

    # Log Message
    Service_Logger.info(f"Handling Device Info ['{ID}']")

def Device_Handler_Error_Log(ID):

    # Log Message
    Service_Logger.info(f"Handling Device Error ['{ID}']")





# Kafka Que Error Log Message
def Kafka_Que_Error_Log():
    
	# Log Message
	Service_Logger.debug("Kafka Que Error.")






# Unknown Log Message
def Unknown_Log(request):

	Service_Logger.error(f"Unknown data come from device. ['{request.client.host}']")


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








def Device_Header_Handler_Error():

    # Log Message
    Service_Logger.error(f"Error -> Handling headers...")

# Log Message
def LOG_Message(Message):
    
	# Log Message
	Service_Logger.info(f"--> {Message}")
