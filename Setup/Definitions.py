# Import Required Libraries
from enum import Enum

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
	def __init__(self, stream_id=0, command_id=0, device_firmware_id=0, new_sim=False, new_modem=False, new_device=False, message=None, iccid=None):

		# Define Variables
		self.stream_id = stream_id
		self.command_id = command_id
		self.device_firmware_id = device_firmware_id
		self.new_sim = new_sim
		self.new_modem = new_modem
		self.new_device = new_device
		self.message = message
		self.iccid = iccid

	# Define Repr Function
	def __repr__(self):
		return (f"StreamData(stream_id={self.stream_id}, command_id={self.command_id}, device_firmware_id={self.device_firmware_id}, new_sim={self.new_sim}, new_modem={self.new_modem}, new_device={self.new_device}), message={self.message}, iccid={self.iccid})")
