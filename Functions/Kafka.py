# Setup Root Path
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Import Packages
from confluent_kafka import Producer

# Define Producer
def delivery_report(err, msg):

    if err is not None:

        print(f'Message delivery failed: {err}')

    else:

        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

# Define Producer
p = Producer({'bootstrap.servers': '172.20.5.3:9092'})

topic = 'Test'
message = 'Hello, Kafka!'

# Produce Message
p.produce(topic, message.encode('utf-8'), callback=delivery_report)

# Poll
p.poll(0)

# Flush
p.flush()
