# Setup Library
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Import Libraries
from Setup.Config import APP_Settings
from Functions import Log, Database_Functions, ICCID_Functions
from Setup import Database, Models, Schema
from confluent_kafka import Consumer, KafkaError
import time
import json
from pydantic import ValidationError

# Define Kafka Consumer
Consumer_Config = {
    'bootstrap.servers': f'{APP_Settings.KAFKA_HOSTNAME}:{APP_Settings.KAFKA_PORT}',
    'group.id': 'RAW_Handler_Group',
    'auto.offset.reset': 'earliest',
	'enable.auto.commit': False,
}

# Define Consumer Class
RAW_Consumer = Consumer(Consumer_Config)

# Define Subscription Function
RAW_Consumer.subscribe([APP_Settings.KAFKA_RAW_TOPIC])

# Define Stream Data Class
class StreamData:

	# Constructor
	def __init__(self, stream_id=0, command_id=0, device_firmware_id=0, new_sim=False, new_modem=False, new_device=False, message=None):

		# Define Variables
		self.stream_id = stream_id
		self.command_id = command_id
		self.device_firmware_id = device_firmware_id
		self.new_sim = new_sim
		self.new_modem = new_modem
		self.new_device = new_device
		self.message = message

	# Define Repr Function
	def __repr__(self):
		return (f"StreamData(stream_id={self.stream_id}, command_id={self.command_id}, device_firmware_id={self.device_firmware_id}, new_sim={self.new_sim}, new_modem={self.new_modem}, new_device={self.new_device}), message={self.message}")

# Define Consumer Topic Loop
try:

	while True:

		# Get Message
		Consumer_Message = RAW_Consumer.poll(timeout=1.0)

		# Check for Message
		if Consumer_Message is None:
			
			# Continue
			continue

		# Check for Error
		if Consumer_Message.error():
			
			# Check for Error
			if Consumer_Message.error().code() == KafkaError._PARTITION_EOF:
				
				# Continue
				continue

			# Check for Error
			elif Consumer_Message.error():
				
				# Log Error
				Log.Terminal_Log('ERROR', f'Consumer Error: {Consumer_Message.error()}')

			# Continue
			continue

		# Get Message
		else:

			# Define Variables
			Stream_Data = StreamData()

			# Get Headers
			Headers = {key: value.decode('utf-8') for key, value in Consumer_Message.headers()}

			# Get Message
			try:

				# Decode Message
				RAW_Message = Consumer_Message.value().decode('utf-8')

				# Check if RAW_Message is valid
				if not RAW_Message:

					# Continue
					continue

				# Parse RAW_Message to dict if it's a JSON string
				if isinstance(RAW_Message, str):

					# Parse RAW_Message
					try:

						# Parse RAW_Message
						RAW_Message = json.loads(RAW_Message)

					# Check for JSONDecodeError
					except json.JSONDecodeError as e:

						# Continue
						continue

				# Ensure RAW_Message is a dict
				if not isinstance(RAW_Message, dict):

					# Continue
					continue

				# Parse Message using Schema
				Stream_Data.message = Schema.Data_Pack(**RAW_Message)

			# Check for Errors
			except (TypeError, json.JSONDecodeError, ValidationError) as e:

				# Continue
				continue

			# Get Command ID
			Stream_Data.command_id = Database_Functions.Get_Command_ID(
				Headers['Command']
			)

			# Get or Create Device Firmware
			Stream_Data.device_firmware_id = Database_Functions.Get_or_Create_Firmware(
				Stream_Data.message.Info.Firmware
			)

			# Check for SIM
			ICCID_Controlled = ICCID_Functions.Verify_and_Strip_ICCID(
				Stream_Data.message.Device.IoT.ICCID
			)

			# Get or Create SIM Existence
			Stream_Data.new_sim = Database_Functions.Get_or_Create_SIM(
				ICCID_Controlled
			)

			# Check for Modem
			Stream_Data.new_modem = Database_Functions.Get_or_Create_Modem(
				Stream_Data.message.Device.IoT.IMEI, 
				Stream_Data.message.Device.IoT.Firmware
			)

			# Check for Device
			Stream_Data.new_device = Database_Functions.Get_or_Create_Device(
				Stream_Data.message.Info.ID,
				Stream_Data.device_firmware_id,
				Stream_Data.message.Device.IoT.IMEI,
				Headers['Device_IP'],
				Headers['Device_Time']
			)

			# Check for Connection Table
			Stream_Data.new_connection = Database_Functions.Get_or_Create_Connection(
				Headers['Device_IP']
			)










			# Define DB
			DB_Module = Database.SessionLocal()

			# Record Stream
			New_Stream = Models.Stream(
				Device_ID = Stream_Data.message.Info.ID,
				Command_ID = Stream_Data.command_id,
				ICCID = ICCID_Controlled,
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
			Stream_ID = New_Stream.Stream_ID

			# Log Message
			Log.Terminal_Log('INFO', f'Stream ID   : {Stream_ID} - [{Headers["Device_ID"]} / {Stream_Data.message.Info.Firmware} / {Stream_Data.new_device}] - [{Headers["Command"]} / {Stream_Data.command_id}] - [{ICCID_Controlled} / {Stream_Data.new_sim}] - [{Stream_Data.message.Device.IoT.IMEI} / {Stream_Data.message.Device.IoT.Firmware} / {Stream_Data.new_modem}]')

			# Commit Message
			RAW_Consumer.commit(asynchronous=False)

except KeyboardInterrupt:
    
	# Consumer Closed Manually
    Log.Terminal_Log('INFO', 'Handler is shutting down...')

finally:

	# Wait for Finish
	time.sleep(2)

	# Close Consumer
	RAW_Consumer.close()
