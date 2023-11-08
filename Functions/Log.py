# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup.Config import APP_Settings
import logging, coloredlogs

# Define Log Colors
coloredlogs.DEFAULT_LOG_LEVEL_COLORS = {
    'INFO': 'white',
    'DEBUG': 'cyan',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red,bg_white',
}

# Set Log Options
Service_Logger = logging.getLogger('Service_Logger')

# Set Log
coloredlogs.install(level='DEBUG', logger=Service_Logger)

# Set Log File
logging.basicConfig(filename=APP_Settings.LOG_FILE, level=logging.INFO, format='%(message)s')

# Set Log Format
Log_Format = "%(asctime)s PostOffice %(message)s"

# Set Log
coloredlogs.install(level='DEBUG', logger=Service_Logger, fmt=Log_Format)

# Log Error Message
def LOG_Error_Message(Message):
    
	# Log Message
	Service_Logger.error(f"--> {Message}")

# Log Message
def Terminal_Log(Type, Message):

	# Control for no type
	if Type == None:

		# Log Message
		Service_Logger.info(f"--> {Message}")

	# Control Type
	if Type == "INFO":
		
		# Log INFO Message
		Service_Logger.info(f"--> {Message}")

	elif Type == "ERROR":

		# Log ERROR Message
		Service_Logger.error(f"--> {Message}")

	elif Type == "DEBUG":

		# Log DEBUG Message
		Service_Logger.debug(f"--> {Message}")

	elif Type == "WARNING":

		# Log WARNING Message
		Service_Logger.warning(f"--> {Message}")

	elif Type == "CRITICAL":

		# Log CRITICAL Message
		Service_Logger.critical(f"--> {Message}")

