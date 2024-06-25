# Setup Library
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Import Libraries
from Setup.Definitions import Variable_Segment as Constants
from Setup import Schema, Definitions, Config, Database, Models
from Functions import Log, Database_Functions, ICCID_Functions
from confluent_kafka import Consumer, KafkaError
from pydantic import ValidationError
import time, json

# Define Kafka Consumer
Rule_Consumer_Config = {
    'bootstrap.servers': f'{Config.APP_Settings.KAFKA_HOSTNAME}:{Config.APP_Settings.KAFKA_PORT}',
    'group.id': 'Rule_Handler_Group',
    'auto.offset.reset': 'earliest',
	'enable.auto.commit': False,
}

# Define Consumer Class
Rule_Consumer = Consumer(Rule_Consumer_Config)

# Define Subscription Function
Rule_Consumer.subscribe([Config.APP_Settings.KAFKA_RAW_TOPIC])

# Log Consumer Start
Log.Terminal_Log('INFO', 'Consumer is starting...')

# Define Consumer Topic Loop
try:

	while True:

		# Get Message
		Consumer_Message = Rule_Consumer.poll(timeout=1.0)

		# Check for Message
		if Consumer_Message is None:

			# Continue
			continue

		# Check for Error
		if Consumer_Message.error():

			# Check for Error
			if Consumer_Message.error().code() == KafkaError._PARTITION_EOF:

				# Continue
				continue

			# Check for Error
			elif Consumer_Message.error():

				# Log Error
				Log.Terminal_Log('ERROR', f'Consumer Error: {Consumer_Message.error()}')

			# Continue
			continue

		# Get Message
		else:

			# Set Message Schema
#			Message = Schema.Data_Pack(**json.loads(Consumer_Message.value().decode('utf-8'))).dict(exclude_none=True)
			Message = Consumer_Message.value().decode('utf-8')

	
			# Log Message
			Log.Terminal_Log('INFO', f'{Message}')
			Log.Terminal_Log('INFO', f'-------------------------------------------------------------')





			# Define DB
			DB_Module = Database.SessionLocal()

			# Get Pack Dictionary
			try:

				# Query all data types
				Data_Type_Query = DB_Module.query(Models.Variable).all()

				# Get Data Type List
				Formatted_Data = [(Variable.Variable_ID, Variable.Variable_Unit) for Variable in Data_Type_Query]

			finally:
				
				# Close Database
				DB_Module.close()

			# Define Found Variables
			Found_Variables = {}

			# Check for Tuple and Extract Variable IDs
			keys_to_check = [var[0] if isinstance(var, tuple) else var for var in Formatted_Data]

			# Get Pack Dictionary
			Pack_Dict = Message

			# Check for Variables
			for variable in keys_to_check:

				# Check for Variable
				if variable in Pack_Dict:

					# Get Value
					value = Pack_Dict[variable]

					# Check for Value
					if value is not None and value != "":

						# Add to Found Variables
						Found_Variables[variable] = value

			#Log Found Variables
			Log.Terminal_Log('INFO', f'Found Variables: {Found_Variables}')










			# Commit Message
			Rule_Consumer.commit(asynchronous=False)

except KeyboardInterrupt:

	# Consumer Closed Manually
    Log.Terminal_Log('INFO', 'Handler is shutting down...')

finally:

	# Wait for Finish
	time.sleep(2)

	# Close Consumer
	Rule_Consumer.close()
