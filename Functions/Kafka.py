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

    # Convert value to JSON format
    json_value = json.dumps(value)
    
    # Encode headers
    Encoded_Headers = [(k, bytes(v, 'utf-8')) for k, v in headers]

    # Produce message to Kafka
    Kafka_Producer.produce(
        topic,
        json_value.encode('utf-8'),
        callback=Delivery_Error_Report,
        headers=Encoded_Headers
    )

    # Poll and flush to ensure delivery
    Kafka_Producer.poll(0)
    Kafka_Producer.flush()
