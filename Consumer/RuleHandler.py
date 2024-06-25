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
Rule_Consumer_Config = {
    'bootstrap.servers': f'{Config.APP_Settings.KAFKA_HOSTNAME}:{Config.APP_Settings.KAFKA_PORT}',
    'group.id': 'Rule_Handler_Group',
    'auto.offset.reset': 'earliest',
	'enable.auto.commit': False,
}

# Define Consumer Class
Rule_Consumer = Consumer(Rule_Consumer_Config)

# Define Subscription Function
Rule_Consumer.subscribe([Config.APP_Settings.KAFKA_RAW_TOPIC])

# Log Consumer Start
Log.Terminal_Log('INFO', 'Consumer is starting...')

# Define Consumer Topic Loop
try:

	while True:

		# Get Message
		Consumer_Message = Rule_Consumer.poll(timeout=1.0)

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

			# Set Message Schema
			Message = Schema.Data_Pack(**json.loads(Consumer_Message.value().decode('utf-8'))).dict(exclude_none=True)

	
			# Log Message
			Log.Terminal_Log('INFO', f'{Message}')
			Log.Terminal_Log('INFO', f'-------------------------------------------------------------')










			# Commit Message
			Rule_Consumer.commit(asynchronous=False)

except KeyboardInterrupt:

	# Consumer Closed Manually
    Log.Terminal_Log('INFO', 'Handler is shutting down...')

finally:

	# Wait for Finish
	time.sleep(2)

	# Close Consumer
	Rule_Consumer.close()
