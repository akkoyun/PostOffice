# Setup Library
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Library Includes
from Setup.Config import APP_Settings
import logging
import os

# Define Formats
Log_Format = "{asctime} [{levelname:^9}] --> {message}"
Log_Formats = {
    logging.DEBUG: Log_Format,
    logging.INFO: f"\33[36m{Log_Format}\33[0m",
    logging.WARNING: f"\33[33m{Log_Format}\33[0m",
    logging.ERROR: f"\33[31m{Log_Format}\33[0m",
    logging.CRITICAL: f"\33[1m\33[31m{Log_Format}\33[0m"
}

# Simple Formatter
class SimpleFormatter(logging.Formatter):
    def __init__(self):
        super().__init__(fmt="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Custom Formatter 
class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = Log_Formats[record.levelno]
        formatter = logging.Formatter(log_fmt, style='{')
        return formatter.format(record)

# Set Handler
Handler = logging.StreamHandler()
Handler.setFormatter(CustomFormatter())
logging.basicConfig(
    level = logging.INFO,
    handlers = [Handler],
)

# Set Log Directory
LOG_DIR = APP_Settings.LOG_DIR
os.makedirs(LOG_DIR, exist_ok=True)

# Set Log File
LOG_FILE = os.path.join(LOG_DIR, "APP_Settings.LOG_FILE")
File_Handler = logging.FileHandler(LOG_FILE)

# Set File Handler
File_Handler.setFormatter(SimpleFormatter())

# Set Logger
Logger = logging.getLogger('PostOffice')

# Add File Handler
Logger.addHandler(File_Handler)

# Terminal Log Message
def Terminal_Log(Type: str, Message: str):

	# Control Type
    if Type == "DEBUG":

        # Log DEBUG Message
        Logger.debug(Message)

    elif Type == "INFO":
		
		# Log INFO Message
        Logger.info(Message)

    elif Type == "ERROR":

		# Log ERROR Message
        Logger.error(Message)

    elif Type == "WARNING":

		# Log WARNING Message
        Logger.warning(Message)

    elif Type == "CRITICAL":

		# Log CRITICAL Message
        Logger.critical(Message)