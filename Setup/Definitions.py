# Import Required Libraries
from enum import Enum, IntEnum

# Define Constants
class Constants:

	# Info Constants
	class INFO:

		# Command Constants
		DEFAULT_COMMAND = 'Unknown'
		COMMAND_ALLOWED = ['Online', 'Timed', 'Alarm', 'Interrupt', 'Oflfine', 'Configuration']
		COMMAND_MIN_LENGTH = 3
		COMMAND_MAX_LENGTH = 10

		# ID Constants
		DEFAULT_ID = "0000000000000000"
		ID_PATTERN = r'^[0-9A-F]{10,16}$'

		# Firmware Constants
		DEFAULT_FIRMWARE = "00.00.00"
		FIRMWARE_PATTERN = r'^[0-9]{2}\.[0-9]{2}\.[0-9]{2}$'

	# Define Battery Constants
	class BATTERY:

		# Define Battery Charge State
		class CHARGE_STATE(IntEnum):
			DISCHARGE = 0
			PRE_CHARGE = 1
			FAST_CHARGE = 2
			CHARGE_DONE = 3
			UNKNOWN = 9

		# Battery Voltage Constants
		VOLTAGE_MIN = 0.0
		VOLTAGE_MAX = 6.0
		DEFAULT_VOLTAGE = 0.0

		# Battery Current Constants
		CURRENT_MIN = -5000.0
		CURRENT_MAX = 5000.0
		DEFAULT_CURRENT = 0.0

		# Full Battery Capacity Constants
		CAPACITY_MIN = 0
		CAPACITY_MAX = 10000
		DEFAULT_CAPACITY = 0

		# Instant Battery Capacity Constants
		INSTANT_CAPACITY_MIN = 0
		INSTANT_CAPACITY_MAX = 10000
		DEFAULT_INSTANT_CAPACITY = 0

		# Battery State of Charge Constants
		SOC_MIN = 0.0
		SOC_MAX = 100.0
		DEFAULT_SOC = 0.0

		# Battery Temperature Constants
		TEMPERATURE_MIN = -50.0
		TEMPERATURE_MAX = 100.0
		DEFAULT_TEMPERATURE = 0.0

	# Define IoT Constants
	class IOT:

		# Define WDS Constants
		class WDS(IntEnum):
			CONNECTION_UNKNOWN = 0
			CONNECTION_2G = 1
			CONNECTION_3G = 2
			CONNECTION_4G = 3
			CONNECTION_TDSCDMA = 4

		# Firmware Version Constants
		FIRMWARE_PATTERN = r'^[0-9]{2}\.[0-9]{2}\.[0-9]{3}$'
		DEFAULT_FIRMWARE = "00.00.000"

		# IMEI Number Constants
		IMEI_PATTERN = r'^[0-9]{10,15}$'
		DEFAULT_IMEI = "000000000000000"
		IMEI_MIN_LENGTH = 10
		IMEI_MAX_LENGTH = 15

		# ICCID Number Constants
		ICCID_MIN_LENGTH = 10
		ICCID_MAX_LENGTH = 20
		ICCID_PATTERN = r'^[0-9]{10,20}$'
		DEFAULT_ICCID = "00000000000000000000"

		# RSSI Signal Level Constants
		RSSI_MIN = -100
		RSSI_MAX = 100
		DEFAULT_RSSI = 0

		# Connection Time Constants
		CONNECTION_TIME_MIN = 0.0
		CONNECTION_TIME_MAX = 100000.0
		DEFAULT_CONNECTION_TIME = 0.0

		# TAC Constants
		TAC_MIN = 0
		TAC_MAX = 65535
		DEFAULT_TAC = 0

		# LAC Constants
		LAC_MIN = 0
		LAC_MAX = 65535
		DEFAULT_LAC = 0

		# Cell ID Constants
		CELL_ID_MIN = 0
		CELL_ID_MAX = 65535
		DEFAULT_CELL_ID = 0

# Command Enum Class
class Command(Enum):

	# Define Enumerations
	Unknown = 0
	Online = 1
	Timed = 2
	Alarm = 3
	Interrupt = 4
	Offline = 5
	Configuration = 6

# Variable Data Segment Enum Class
class Variable_Segment(Enum):

    # Define Enumerations
    Unknown = 0
    Device = 1
    Power = 2
    GSM = 3
    Location = 4
    Environment = 5
    Water = 6
    Energy = 7
    FOTA = 9

# Define Stream Data Class
class StreamData:

	# Constructor
	def __init__(self, stream_id=0, command_id=0, device_firmware_id=0, sim_id=0, new_modem=False, new_device=False, message=None, iccid=None):

		# Define Variables
		self.stream_id = stream_id
		self.command_id = command_id
		self.device_firmware_id = device_firmware_id
		self.sim_id = sim_id
		self.new_modem = new_modem
		self.new_device = new_device
		self.message = message
		self.iccid = iccid

	# Define Repr Function
	def __repr__(self):
		return (f"StreamData(stream_id={self.stream_id}, command_id={self.command_id}, device_firmware_id={self.device_firmware_id}, sim_id={self.sim_id}, new_modem={self.new_modem}, new_device={self.new_device}), message={self.message}, iccid={self.iccid})")
