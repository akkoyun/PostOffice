# Setup Library
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Import Libraries
from Setup.Config import APP_Settings
from Functions import Log, FastApi_Functions, Database_Functions, Kafka
from Setup import Database, Models, Schema
from confluent_kafka import Consumer, KafkaException, KafkaError
import time

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

# Define DB
DB_Module = Database.SessionLocal()

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
			Headers = Consumer_Message.headers()

			# Headers Dict Conversion
			Headers_Dict = {key: value.decode('utf-8') for key, value in Headers}

			# Get Message Value
			Message = Consumer_Message.value().decode('utf-8')

			# Define Variables
			Database_Command_ID = None
			Database_SIM_ID = None
			New_SIM	= False

			# Check for Command
			if Headers_Dict['Command'] is not None:

				# Check for Command Table
				try:

					# Control Service
					Command_Query = (DB_Module.query(Models.Command).filter(
						Models.Command.Command.like(Headers_Dict['Command'])
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

			else:

				# Set Command ID
				Command_ID = 0

			# Check for ICCID
			if Schema.Data_Pack.Device.IoT.ICCID is not None:

				# Check for SIM Table
				try:

					# Control Service
					SIM_Query = (DB_Module.query(Models.SIM).filter(
						Models.SIM.ICCID.like(Schema.Data_Pack.Device.IoT.ICCID)
					).first())

					# SIM Found
					if SIM_Query is not None:

						# Get SIM ID
						Database_SIM_ID = SIM_Query.SIM_ID

					else:

						# Create New SIM
						New_SIM = Models.SIM(
							ICCID = Schema.Data_Pack.Device.IoT.ICCID,
							Operator_ID = 286 # Daha sonra düzeltilecek şu an manuel olarak yazıldı
						)

						# Add SIM to DataBase
						DB_Module.add(New_SIM)

						# Commit DataBase
						DB_Module.commit()

						# Refresh DataBase
						DB_Module.refresh(New_SIM)

						# Get SIM ID
						Database_SIM_ID = New_SIM.SIM_ID

				finally:

					# Close Database
					DB_Module.close()

			else:

				# Set SIM ID
				Database_SIM_ID = 0




















			# Log Message
			Log.Terminal_Log('INFO', f'Topic       : {Consumer_Message.topic()}')
			Log.Terminal_Log('INFO', f'Command     : {Headers_Dict["Command"]} - [{Command_ID}]')
			Log.Terminal_Log('INFO', f'Device ID   : {Headers_Dict["Device_ID"]}')
			Log.Terminal_Log('INFO', f'Device Time : {Headers_Dict["Device_Time"]}')
			Log.Terminal_Log('INFO', f'Device IP   : {Headers_Dict["Device_IP"]}')
			Log.Terminal_Log('INFO', f'ICCID	   : {Schema.Data_Pack.Device.IoT.ICCID} - [{Database_SIM_ID}]')
			Log.Terminal_Log('INFO', f'Size        : {Headers_Dict["Size"]}')
			Log.Terminal_Log('INFO', f'-------------------')
			Log.Terminal_Log('INFO', f'Message     : {Message}')
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
