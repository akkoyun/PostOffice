# Setup Library
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Import Libraries
from Setup.Definitions import Variable_Segment as Constants
from Setup import Schema, Definitions, Config
from Functions import Log, Database_Functions, ICCID_Functions
from confluent_kafka import Consumer, KafkaError
from pydantic import ValidationError
import time, json

# Define Kafka Consumer
Consumer_Config = {
    'bootstrap.servers': f'{Config.APP_Settings.KAFKA_HOSTNAME}:{Config.APP_Settings.KAFKA_PORT}',
    'group.id': 'RAW_Handler_Group',
    'auto.offset.reset': 'earliest',
	'enable.auto.commit': False,
}

# Define Consumer Class
RAW_Consumer = Consumer(Consumer_Config)

# Define Subscription Function
RAW_Consumer.subscribe([Config.APP_Settings.KAFKA_RAW_TOPIC])

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
			Log.Terminal_Log('INFO', f'Consumer Message: {Consumer_Message.value()}')
			Log.Terminal_Log('INFO', f'-------------------------------------------------------------')

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
