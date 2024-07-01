# Setup Library
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Import Libraries
from Setup import Config, Database, Models
from Functions import Log, Kafka, Database_Functions
from confluent_kafka import Consumer
import time, operator

# Define Kafka Consumer
KPI_Consumer_Config = {
	'bootstrap.servers': f'{Config.APP_Settings.KAFKA_HOSTNAME}:{Config.APP_Settings.KAFKA_PORT}',
	'group.id': 'Rule_Handler_Group',
	'auto.offset.reset': 'earliest',
	'enable.auto.commit': False,
}

# Define Consumer Class
KPI_Consumer = Consumer(KPI_Consumer_Config)

# Define Subscription Function
KPI_Consumer.subscribe([Config.APP_Settings.KAFKA_RAW_TOPIC])

# Log Consumer Start
Log.Terminal_Log('INFO', 'KPI Consumer is starting...')

# Define Consumer Topic Loop
try:

	while True:

		# Get Message
		Kafka_Message = Kafka.Get_Message_From_Topic(KPI_Consumer)

		# Check for Message
		if Kafka_Message is None:

			# Continue
			continue

		# Set Message
		Message, Headers, Consumer_Message = Kafka_Message

		# Get Data Packs
		Device = Message.get('Device', {})
		Power_Pack = Device.get('Power', {})
		IoT_Pack = Device.get('IoT', {})
		Payload = Message.get('Payload', {})

		# Define DB
		DB_Module = Database.SessionLocal()

		# Get All Variables
		Formatted_Data = Database_Functions.Get_All_Variables()

		# Define Found Variables
		Found_Variables = {}

		# Check for Tuple and Extract Variable IDs
		Keys_To_Check = [var[0] if isinstance(var, tuple) else var for var in Formatted_Data]


		Log.Terminal_Log('INFO', f'Keys to Check : {Keys_To_Check}')
		Log.Terminal_Log('INFO', f'-------------------------------------------------------------')











		# Control for RMS Voltage Imbalance
#		if (Stream_Data.message.Payload.VRMS_R is not None and Stream_Data.message.Payload.VRMS_S is not None and Stream_Data.message.Payload.VRMS_T is not None) and Stream_Data.message.Payload.VRMS_IMB is None:

			# Calculate Voltage Imbalance
#			Voltage_Imbalance = (max(Stream_Data.message.Payload.VRMS_R, Stream_Data.message.Payload.VRMS_S, Stream_Data.message.Payload.VRMS_T) - min(Stream_Data.message.Payload.VRMS_R, Stream_Data.message.Payload.VRMS_S, Stream_Data.message.Payload.VRMS_T)) / max(Stream_Data.message.Payload.VRMS_R, Stream_Data.message.Payload.VRMS_S, Stream_Data.message.Payload.VRMS_T)

			# Log Message
#			Log.Terminal_Log('WARNING', f'Voltage Imbalance Detected : {Voltage_Imbalance}')





















		# Log Message
		Log.Terminal_Log('INFO', f'-------------------------------------------------------------')

		# Commit Message
		KPI_Consumer.commit(asynchronous=False)

except KeyboardInterrupt:

	# Consumer Closed Manually
	Log.Terminal_Log('INFO', 'Handler is shutting down...')

finally:

	# Wait for Finish
	time.sleep(2)

	# Close Consumer
	KPI_Consumer.close()
