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
			Database_Command_ID = 0
			New_SIM	= False

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
							Operator_ID = 286 # Daha sonra düzeltilecek şu an manuel olarak yazıldı
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




















			# Log Message
			Log.Terminal_Log('INFO', f'Topic       : {Consumer_Message.topic()}')
			Log.Terminal_Log('INFO', f'Command     : {Headers["Command"]} - [{Database_Command_ID}]')
			Log.Terminal_Log('INFO', f'Device ID   : {Headers["Device_ID"]}')
			Log.Terminal_Log('INFO', f'Device Time : {Headers["Device_Time"]}')
			Log.Terminal_Log('INFO', f'Device IP   : {Headers["Device_IP"]}')
			Log.Terminal_Log('INFO', f'ICCID	   : {Message.Device.IoT.ICCID} - [{New_SIM}]')
			Log.Terminal_Log('INFO', f'Size        : {Headers["Size"]}')
			Log.Terminal_Log('INFO', f'-------------------')




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
