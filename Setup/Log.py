# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from .Config import APP_Settings
import logging, coloredlogs
from . import Database, Models, Log

# Set Log Options
Service_Logger = logging.getLogger(__name__)
logging.basicConfig(filename=APP_Settings.POSTOFFICE_LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

# Set Log Colored
coloredlogs.install(level='DEBUG', logger=Service_Logger)

# Log Message
def LOG_Message(Message):
    
	# Log Message
	Service_Logger.info(f"--> {Message}")

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

