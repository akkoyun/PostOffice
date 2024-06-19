# Setup Root Path
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Import Packages
from confluent_kafka import Producer
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
def Send_To_Topic(Topic: str, Value: Schema.Data_Pack, Headers, Partition=0):

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
        headers=Encoded_Headers,
        key=Value.Info.ID.encode('utf-8')
    )

    # Poll and flush to ensure delivery
    Kafka_Producer.poll(0)
    Kafka_Producer.flush()
