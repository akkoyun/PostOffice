# Setup Root Path
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Import Packages
from confluent_kafka import Producer, KafkaError
from Setup.Config import APP_Settings
from Functions import Log
from Setup import Schema
import json

# Define Kafka Producer
Kafka_Producer = Producer({
    'bootstrap.servers': f'{APP_Settings.KAFKA_HOSTNAME}:{APP_Settings.KAFKA_PORT}',
    'acks': 'all',
    'compression.type': 'gzip',
    'retries': 5
})

# Define Delivery Report
def Delivery_Error_Report(err, msg):

	# Check for Error
	if err is not None:

		# Log Error
		Log.Terminal_Log("ERROR", f"Message delivery failed: {err}")

# Send To Topic Function
def Send_To_Topic(Topic: str, Value, Headers, Partition=0):

    # Convert value to JSON format if it's a dict or list, otherwise use it as is
    if isinstance(Value, (dict, list)):
        JSON_Value = json.dumps(Value)
    else:
        JSON_Value = Value

    # Encode headers if they are not already in bytes
    Encoded_Headers = [(k, v if isinstance(v, bytes) else bytes(v, 'utf-8')) for k, v in Headers]

    # Produce message to Kafka
    Kafka_Producer.produce(
        Topic,
        JSON_Value.encode('utf-8') if isinstance(JSON_Value, str) else JSON_Value,
        callback=Delivery_Error_Report,
        partition=Partition,
        headers=Encoded_Headers
    )

    # Poll and flush to ensure delivery
    Kafka_Producer.poll(0)
    Kafka_Producer.flush()

# Get Kafka Message Function
def Get_Message_From_Topic(consumer):

	# Get Message
	Consumer_Message = consumer.poll(timeout=1.0)

	# Check for Message
	if Consumer_Message is None:
		return None

	# Check for Error
	if Consumer_Message.error():

		# Check for Error
		if Consumer_Message.error().code() == KafkaError._PARTITION_EOF:

			# Continue
			return None

		# Check for Error
		else:

			# Log Error
			Log.Terminal_Log('ERROR', f'Consumer Error: {Consumer_Message.error()}')

		# Continue
			return None

	# Decode and parse the message
	try:

		# Decode Message
		Message = json.loads(Consumer_Message.value().decode('utf-8'))

	# Check for JSON Decode Error
	except json.JSONDecodeError as e:

		# Log Error
		Log.Terminal_Log('ERROR', f'JSON Decode Error: {e}')

		# Continue
		return None

	# Get Headers
	Headers = {key: value.decode('utf-8') for key, value in Consumer_Message.headers()}

	return Message, Headers, Consumer_Message
