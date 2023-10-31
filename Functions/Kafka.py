# Library Includes
from Functions import Log
from Setup.Config import APP_Settings
from Setup import Schema
from kafka import KafkaConsumer, KafkaProducer
import json
import time

# Kafka Producers
Kafka_Producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('utf-8'), bootstrap_servers=f'{APP_Settings.KAFKA_HOSTNAME}:{APP_Settings.KAFKA_PORT}')

# Kafka Callbacks
def Send_Success(record_metadata):

	# Log Message
	Log.Terminal_Log("INFO", f"Send to Kafka Queue: {record_metadata.topic} / {record_metadata.partition} / {record_metadata.offset}")

# Kafka Callbacks
def Send_Error(excp):

	# Log Message
	Log.Terminal_Log("ERROR", f"Kafka Send Error: {excp}")

# Send to Topic
def Send_To_Topic(topic, value, headers, max_retries=3, delay=5):

    # Define Retry Counter
    Retries = 0

    # Try to Send Message
    while Retries < max_retries:

        try:

            # Send Message to Queue
            Kafka_Producer.send(topic, value=value, headers=headers).add_callback(Send_Success).add_errback(Send_Error)

            # Break Loop
            return

        except Exception as e:

            # Log Message
            Log.Terminal_Log("INFO", f"Failed to send message to {topic}. Attempt {Retries+1} of {max_retries}. Error: {e}")

            # Increment Retry Counter
            Retries += 1

            # Sleep
            time.sleep(delay)

    # Log Message
    Log.Terminal_Log("INFO", f"Failed to send message to {topic} after {max_retries} attempts.")

