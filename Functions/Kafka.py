# Setup Root Path
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Import Packages
from confluent_kafka import Producer
from Setup.Config import APP_Settings
from Functions import Log
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
def Send_To_Topic(topic: str, value, headers):

    # Convert value to JSON format if it's a dict or list, otherwise use it as is
    if isinstance(value, (dict, list)):
        json_value = json.dumps(value)
    else:
        json_value = value

    # Encode headers if they are not already in bytes
    Encoded_Headers = [(k, v if isinstance(v, bytes) else bytes(v, 'utf-8')) for k, v in headers]

    # Produce message to Kafka
    Kafka_Producer.produce(
        topic,
        json_value.encode('utf-8') if isinstance(json_value, str) else json_value,
        callback=Delivery_Error_Report,
        headers=Encoded_Headers
    )

    # Poll and flush to ensure delivery
    Kafka_Producer.poll(0)
    Kafka_Producer.flush()
