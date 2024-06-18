# Setup Root Path
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Import Packages
from confluent_kafka import Producer
from Setup.Config import APP_Settings
from Functions import Log

print(APP_Settings.dict())

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

# Define Topic and Message
Topic = 'Test'
Message = 'Hello, Kafka!'
Headers = [
    ('header_key_1', 'header_value_1'),
    ('header_key_2', 'header_value_2'),
    ('header_key_3', 'header_value_3')
]

# Produce Message
Kafka_Producer.produce(
    Topic,
    Message.encode('utf-8'),
    callback=Delivery_Error_Report,
    headers=Headers
)

# Poll and Flush
Kafka_Producer.poll(0)
Kafka_Producer.flush()
