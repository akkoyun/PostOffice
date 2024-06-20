# Setup Library
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Import Libraries
from Setup.Config import APP_Settings
from Functions import Log, FastApi_Functions, Database_Functions, Kafka
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

			# Log Message
			Log.Terminal_Log('INFO', f'Topic : {Consumer_Message.topic()}')

			# Log Message
			Log.Terminal_Log('INFO', f'-------------------')

			# Get Headers
			Headers = Consumer_Message.headers()

			# Headers Dict Conversion
			Headers_Dict = {key: value.decode('utf-8') for key, value in Headers}

			# Log Message
			Log.Terminal_Log('INFO', f'Command     : {Headers_Dict["Command"]}')
			Log.Terminal_Log('INFO', f'Device ID   : {Headers_Dict["Device_ID"]}')
			Log.Terminal_Log('INFO', f'Device Time : {Headers_Dict["Device_Time"]}')
			Log.Terminal_Log('INFO', f'Device IP   : {Headers_Dict["Device_IP"]}')
			Log.Terminal_Log('INFO', f'Size        : {Headers_Dict["Size"]}')

			# Log Message
			Log.Terminal_Log('INFO', f'-------------------')

			# Get Message Value
			Message = Consumer_Message.value().decode('utf-8')

			# Log Message
			Log.Terminal_Log('INFO', f'Message : {Message}')

			# Log Message
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
