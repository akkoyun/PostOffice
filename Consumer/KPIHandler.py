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
	'group.id': 'KPI_Handler_Group',
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

	# Loop Consumer
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

		# Function To Check Variables in a Given Pack
		def Check_Variables_in_Pack(pack, pack_name):

			# Check for Variables
			for variable in Keys_To_Check:

				# Check for Variable
				if variable in pack:

					# Get Value
					value = pack[variable]

					# Check for Value
					if value is not None and value != "":

						# Add to Found Variables
						Found_Variables[variable] = value

		# Check Variables in Packs
		Check_Variables_in_Pack(Power_Pack, 'Power_Pack')
		Check_Variables_in_Pack(IoT_Pack, 'IoT_Pack')
		Check_Variables_in_Pack(Payload, 'Payload')








		# Control for VRMS_R, VRMS_S and VRMS_T
		if (Found_Variables.get("VRMS_R") is not None and Found_Variables.get("VRMS_S") is not None and Found_Variables.get("VRMS_T") is not None) and Found_Variables.get("VRMS_IMB") is None:

			# Set Variable
			VRMS_Array = [Found_Variables.get("VRMS_R"), Found_Variables.get("VRMS_S"), Found_Variables.get("VRMS_T")]

			# Calculate Valuse
			MAX_VRMS_Value = max(VRMS_Array)
			MIN_VRMS_Value = min(VRMS_Array)
			AVG_VRMS_Value = sum(VRMS_Array) / len(VRMS_Array)
			Imbalance = ((MAX_VRMS_Value - MIN_VRMS_Value) / AVG_VRMS_Value) * 100

			# Log Imbalance
			Log.Terminal_Log('INFO', f'VRMS_IMB : {Imbalance}')
			










		# Log Line
		Log.Terminal_Log('INFO', '---------------------------------------------------------------')

		# Commit Message
		KPI_Consumer.commit(asynchronous=False)

# Check for Keyboard Interrupt
except KeyboardInterrupt:

	# Consumer Closed Manually
	Log.Terminal_Log('INFO', 'Handler is shutting down...')

# Check for Finally
finally:

	# Wait for Finish
	time.sleep(2)

	# Close Consumer
	KPI_Consumer.close()

	# Log Consumer End
	Log.Terminal_Log('INFO', 'Consumer is closed.')
