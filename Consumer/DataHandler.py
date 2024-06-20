# Setup Library
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Import Libraries
from Setup.Config import APP_Settings
from Functions import Log
from Setup import Database, Models, Schema
from confluent_kafka import Consumer, KafkaError
import time
import json
from pydantic import ValidationError

# Define Topic
RAW_Consumer_Topic = 'RAW'

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
RAW_Consumer.subscribe([RAW_Consumer_Topic])

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

			# Get Headers
			Headers = {key: value.decode('utf-8') for key, value in Consumer_Message.headers()}

			# Declare Message
			Message = None

			# Get Message
			try:

				# Decode Message
				RAW_Message = Consumer_Message.value().decode('utf-8')

				# Check if RAW_Message is valid
				if not RAW_Message:
					continue

				# Parse RAW_Message to dict if it's a JSON string
				if isinstance(RAW_Message, str):
					try:
						RAW_Message = json.loads(RAW_Message)
					except json.JSONDecodeError as e:
						continue

				# Ensure RAW_Message is a dict
				if not isinstance(RAW_Message, dict):
					continue

				# Parse Message using Schema
				Message = Schema.Data_Pack(**RAW_Message)

			except (TypeError, json.JSONDecodeError, ValidationError) as e:
				continue

			# Define Variables
			Stream_ID = 0
			Database_Command_ID = 0
			Database_Device_Firmware_ID = 0
			New_SIM	= False
			New_Modem = False
			New_Device = False
			Database_Connection_ID = 0

			# Check for Command
			if Headers['Command'] is not None:

				# Check for Command Table
				try:

					# Define DB
					DB_Module = Database.SessionLocal()

					# Control Service
					Command_Query = (DB_Module.query(Models.Command).filter(
						Models.Command.Command.like(Headers['Command'])
					).first())

					# Command Found
					if Command_Query is not None:

						# Get Command ID
						Database_Command_ID = Command_Query.Command_ID

					else:

						# Set Command ID
						Database_Command_ID = 0

				finally:

					# Close Database
					DB_Module.close()

			# Check for ICCID
			if Message.Device.IoT.ICCID is not None:

				# Remove Last 1 Digit from ICCID
				Message.Device.IoT.ICCID = Message.Device.IoT.ICCID[:-1]

				# Check for SIM Table
				try:

					# Define DB
					DB_Module = Database.SessionLocal()

					# Control Service
					SIM_Query = (DB_Module.query(Models.SIM).filter(
						Models.SIM.ICCID.like(Message.Device.IoT.ICCID)
					).first())

					# SIM Found
					if SIM_Query is None:

						# Create New SIM
						New_SIM = Models.SIM(
							ICCID = Message.Device.IoT.ICCID,
							Operator_ID = 1492 # Daha sonra düzeltilecek şu an manuel olarak yazıldı
						)

						# Add SIM to DataBase
						DB_Module.add(New_SIM)

						# Commit DataBase
						DB_Module.commit()

						# Refresh DataBase
						DB_Module.refresh(New_SIM)

						# Set New SIM
						New_SIM = True

				finally:

					# Close Database
					DB_Module.close()

			# Check for Version
			if Message.Info.Firmware is not None:

				# Check for Version Table
				try:

					# Define DB
					DB_Module = Database.SessionLocal()

					# Control Service
					Version_Query = (DB_Module.query(Models.Version).filter(
						Models.Version.Firmware.like(Message.Info.Firmware)
					).first())

					# Version Found
					if Version_Query is None:

						# Create New Version
						New_Version = Models.Version(
							Firmware = Message.Info.Firmware
						)

						# Add Version to DataBase
						DB_Module.add(New_Version)

						# Commit DataBase
						DB_Module.commit()

						# Refresh DataBase
						DB_Module.refresh(New_Version)

						# Get Device Firmware ID
						Database_Device_Firmware_ID = New_Version.Version_ID

					else:

						# Get Device Firmware ID
						Database_Device_Firmware_ID = Version_Query.Version_ID

				finally:

					# Close Database
					DB_Module.close()

			# Check for IMEI
			if Message.Device.IoT.IMEI is not None:

				# Check for Device Table
				try:

					# Define DB
					DB_Module = Database.SessionLocal()

					# Control Service
					Modem_Query = (DB_Module.query(Models.Modem).filter(
						Models.Modem.IMEI.like(Message.Device.IoT.IMEI)
					).first())

					# Device Found
					if Modem_Query is None:

						# Create New Device
						New_Modem = Models.Modem(
							IMEI = Message.Device.IoT.IMEI,
							Model_ID = 0,
							Manufacturer_ID = 21, # Daha sonra düzenlenecek
							Firmware = Message.Device.IoT.Firmware
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

						if Modem_Query.Firmware != Message.Device.IoT.Firmware:

							# Update Device Firmware
							Modem_Query.Firmware = Message.Device.IoT.Firmware

							# Commit DataBase
							DB_Module.commit()

				finally:

					# Close Database
					DB_Module.close()

			# Check for Device
			if Message.Info.ID is not None:

				# Check for Device Table
				try:

					# Define DB
					DB_Module = Database.SessionLocal()

					# Control Service
					Device_Query = (DB_Module.query(Models.Device).filter(
						Models.Device.Device_ID.like(Message.Info.ID)
					).first())

					# Device Found
					if Device_Query is None:

						# Create New Device
						New_Device = Models.Device(
							Device_ID = Message.Info.ID,
							Status_ID = 0,
							Version_ID = Database_Device_Firmware_ID,
							Project_ID = 0,
							Model_ID = 0,
							Manufacturer_ID = 11, # Daha sonra düzenlenecek
							IMEI = Message.Device.IoT.IMEI,
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
						New_Device = True

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

						# Get Connection ID
						Database_Connection_ID = New_Connection.Connection_ID

					else:

						# Get Connection ID
						Database_Connection_ID = Connection_Query.Connection_ID

				finally:

					# Close Database
					DB_Module.close()

			# Define DB
			DB_Module = Database.SessionLocal()

			# Record Stream
			New_Stream = Models.Stream(
				Device_ID = Message.Info.ID,
				Command_ID = Database_Command_ID,
				ICCID = Message.Device.IoT.ICCID,
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
			Log.Terminal_Log('INFO', f'Stream ID   : {Stream_ID} - [{Headers["Device_ID"]} / {New_Device}] - [{Headers["Command"]} / {Database_Command_ID}] - [{Message.Device.IoT.ICCID} / {New_SIM}] - [{Message.Device.IoT.IMEI} / {New_Modem}]') 

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
