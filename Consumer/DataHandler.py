# Setup Library
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Import Libraries
from Setup.Config import APP_Settings
from Functions import Log, Database_Functions
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
			Stream_Data.command_id = Database_Functions.Get_Command_ID(Headers['Command'])

			# Get or Create SIM
			Stream_Data.new_sim = Database_Functions.Get_or_Create_SIM(Stream_Data.message.Device.IoT.ICCID)








			# Check for Version
			if Stream_Data.message.Info.Firmware is not None:

				# Check for Version Table
				try:

					# Define DB
					DB_Module = Database.SessionLocal()

					# Control Service
					Version_Query = (DB_Module.query(Models.Version).filter(
						Models.Version.Firmware.like(Stream_Data.message.Info.Firmware)
					).first())

					# Version Found
					if Version_Query is None:

						# Create New Version
						New_Version = Models.Version(
							Firmware = Stream_Data.message.Info.Firmware,
						)

						# Add Version to DataBase
						DB_Module.add(New_Version)

						# Commit DataBase
						DB_Module.commit()

						# Refresh DataBase
						DB_Module.refresh(New_Version)

						# Get Device Firmware ID
						Stream_Data.device_firmware_id = New_Version.Version_ID

					else:

						# Get Device Firmware ID
						Stream_Data.device_firmware_id = Version_Query.Version_ID

				finally:

					# Close Database
					DB_Module.close()

			# Check for IMEI
			if Stream_Data.message.Device.IoT.IMEI is not None:

				# Check for Device Table
				try:

					# Define DB
					DB_Module = Database.SessionLocal()

					# Control Service
					Modem_Query = (DB_Module.query(Models.Modem).filter(
						Models.Modem.IMEI.like(Stream_Data.message.Device.IoT.IMEI)
					).first())

					# Device Found
					if Modem_Query is None:

						# Create New Device
						New_Modem = Models.Modem(
							IMEI = Stream_Data.message.Device.IoT.IMEI,
							Model_ID = 0,
							Manufacturer_ID = 21, # Daha sonra düzenlenecek
							Firmware = Stream_Data.message.Device.IoT.Firmware,
						)

						# Add Device to DataBase
						DB_Module.add(New_Modem)

						# Commit DataBase
						DB_Module.commit()

						# Refresh DataBase
						DB_Module.refresh(New_Modem)

						# Set New Device
						New_Modem = True
					
					else:

						if Modem_Query.Firmware != Stream_Data.message.Device.IoT.Firmware:

							# Update Device Firmware
							Modem_Query.Firmware = Stream_Data.message.Device.IoT.Firmware

							# Commit DataBase
							DB_Module.commit()

				finally:

					# Close Database
					DB_Module.close()

			# Check for Device
			if Stream_Data.message.Info.ID is not None:

				# Check for Device Table
				try:

					# Define DB
					DB_Module = Database.SessionLocal()

					# Control Service
					Device_Query = (DB_Module.query(Models.Device).filter(
						Models.Device.Device_ID.like(Stream_Data.message.Info.ID)
					).first())

					# Device Found
					if Device_Query is None:

						# Create New Device
						New_Device = Models.Device(
							Device_ID = Stream_Data.message.Info.ID,
							Status_ID = 0,
							Version_ID = Stream_Data.device_firmware_id,
							Project_ID = 0,
							Model_ID = 0,
							Manufacturer_ID = 11, # Daha sonra düzenlenecek
							IMEI = Stream_Data.message.Device.IoT.IMEI,
							Last_Connection_IP = Headers['Device_IP'],
							Last_Connection_Time = Headers['Device_Time'],
						)

						# Add Device to DataBase
						DB_Module.add(New_Device)

						# Commit DataBase
						DB_Module.commit()

						# Refresh DataBase
						DB_Module.refresh(New_Device)

						# Set New Device
						Stream_Data.new_device = True

					else:

						# Update Device
						Device_Query.Last_Connection_IP = Headers['Device_IP']
						Device_Query.Last_Connection_Time = Headers['Device_Time']

						# Commit DataBase
						DB_Module.commit()

				finally:

					# Close Database
					DB_Module.close()

			# Check for Connection Table
			if Headers['Device_IP'] is not None:

				# Check for Connection Table
				try:

					# Define DB
					DB_Module = Database.SessionLocal()

					# Control Service
					Connection_Query = (DB_Module.query(Models.Connection).filter(
						Models.Connection.IP_Address.like(Headers['Device_IP'])
					).first())

					# Connection Found
					if Connection_Query is None:

						# Create New Connection
						New_Connection = Models.Connection(
							IP_Address = Headers['Device_IP'],
							IP_Pool = 0,
						)

						# Add Connection to DataBase
						DB_Module.add(New_Connection)

						# Commit DataBase
						DB_Module.commit()

						# Refresh DataBase
						DB_Module.refresh(New_Connection)

				finally:

					# Close Database
					DB_Module.close()

			# Define DB
			DB_Module = Database.SessionLocal()

			# Record Stream
			New_Stream = Models.Stream(
				Device_ID = Stream_Data.message.Info.ID,
				Command_ID = Stream_Data.command_id,
				ICCID = Stream_Data.message.Device.IoT.ICCID,
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
			Log.Terminal_Log('INFO', f'Stream ID   : {Stream_ID} - [{Headers["Device_ID"]} / {Stream_Data.message.Info.Firmware} / {Stream_Data.new_device}] - [{Headers["Command"]} / {Stream_Data.command_id}] - [{Stream_Data.message.Device.IoT.ICCID} / {Stream_Data.new_sim}] - [{Stream_Data.message.Device.IoT.IMEI} / {Stream_Data.message.Device.IoT.Firmware} / {Stream_Data.new_modem}]')

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
