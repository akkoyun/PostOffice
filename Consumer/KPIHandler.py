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

			# Define Variables
			Stream_Data = Definitions.StreamData()

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














			# Control for RMS Voltage Imbalance
			if (Stream_Data.message.Payload.VRMS_R is not None and Stream_Data.message.Payload.VRMS_S is not None and Stream_Data.message.Payload.VRMS_T is not None) and Stream_Data.message.Payload.VRMS_IMB is None:

				# Calculate Voltage Imbalance
				Voltage_Imbalance = (max(Stream_Data.message.Payload.VRMS_R, Stream_Data.message.Payload.VRMS_S, Stream_Data.message.Payload.VRMS_T) - min(Stream_Data.message.Payload.VRMS_R, Stream_Data.message.Payload.VRMS_S, Stream_Data.message.Payload.VRMS_T)) / max(Stream_Data.message.Payload.VRMS_R, Stream_Data.message.Payload.VRMS_S, Stream_Data.message.Payload.VRMS_T)

				# Log Message
				Log.Terminal_Log('WARNING', f'Voltage Imbalance Detected : {Voltage_Imbalance}')





















			# Log Message
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
