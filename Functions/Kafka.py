# Setup Root Path
import sys
sys.path.append('/home/postoffice/PostOffice/src')

from confluent_kafka import Producer

p = Producer({'bootstrap.servers': '172.20.5.3:9092'}) 

def delivery_report(err, msg):
	if err is not None:
		print(f'Message delivery failed: {err}')
	else:
		print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

topic = 'Test'
message = 'Hello, Kafka!'

p.produce(topic, message.encode('utf-8'), callback=delivery_report)
p.poll(0)
p.flush()
