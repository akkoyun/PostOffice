# Setup Root Path
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Library Includes
from Functions import Log
from Setup.Config import APP_Settings
from kafka import KafkaProducer
import json
import time

# Kafka Producers
Kafka_Producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('utf-8'), bootstrap_servers=f'{APP_Settings.KAFKA_HOSTNAME}:{APP_Settings.KAFKA_PORT}')

# Send to Topic
def Send_To_Topic(topic: str, value, headers, max_retries=3, delay=5):

    # Define Retry Counter
    Retries = 0

    # Try to Send Message
    while Retries < max_retries:

        try:

            # Send Message to Queue
#            Kafka_Producer.send(topic, value=value, headers=headers).add_callback(Send_Success).add_errback(Send_Error)
            Kafka_Producer.send(topic, value=value, headers=headers)

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


# Send Test
Send_To_Topic("Test", {"Test": "Test"}, {"Test": "Test"})