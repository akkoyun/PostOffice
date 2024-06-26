# Setup Library
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Import Libraries
from Setup.Definitions import Variable_Segment as Constants
from Setup import Schema, Definitions, Config, Database, Models
from Functions import Log, Database_Functions, ICCID_Functions
from confluent_kafka import Consumer, KafkaError
from pydantic import ValidationError
import time, json, operator

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





def evaluate_condition(value, condition):

	# Define Operators
	ops = {
		'>': operator.gt,
		'<': operator.lt,
		'>=': operator.ge,
		'<=': operator.le,
		'==': operator.eq,
		'!=': operator.ne
	}

	# Check for Condition
	for op_str, op_func in ops.items():

		# Check for Operator
		if op_str in condition:

			# Check for Value
			cond_value = float(condition.split(op_str)[-1].strip())

			# Check for Operator
			return op_func(value, cond_value)

	# Return False
	return False

def evaluate_composite_rules(data):

	# Record Measurements
	try:

		# Define DB
		with Database.SessionLocal() as DB_Module:

			# Get Rules
			Rule_Query = DB_Module.query(Models.Rules).all()

			for Rule in Rule_Query:

				# Get Rule ID
				Rule_ID = Rule.Rule_ID

				# Get Rule Action
				Rule_Action = Rule.Rule_Action_ID

				# Get Rule Chain
				Rule_Chain = DB_Module.query(Models.RuleChain).filter(Models.RuleChain.Rule_ID == Rule_ID).all()

				# Define Condition Check
				Condition_Check = True

				# Check for Rule Chain
				for Chain in Rule_Chain:

					# Get Chain Variables
					Device_ID = Chain.Device_ID
					Variable_ID = Chain.Variable_ID
					Condition = Chain.Rule_Condition

					# Check for Device ID and Variable ID
					if Device_ID in data and Variable_ID in data[Device_ID]:

						# Get Value
						Value = data[Device_ID][Variable_ID]

						# Evaluate Condition
						if not evaluate_condition(Value, Condition):

							# Set Condition Check
							Condition_Check = False

							# Break Loop
							break

					# Check for Device ID and Variable ID
					else:

						# Set Condition Check
						Condition_Check = False

						# Break Loop
						break

				# Check for Condition Check
				if Condition_Check:

					# Log Rule Action
					Log.Terminal_Log('INFO', f'Rule Action: {Rule_Action}')

	except Exception as e:
		
		# Log Error
		Log.Terminal_Log('ERROR', f'Error: {e}')











# Define Consumer Topic Loop
try:

	# Loop Consumer
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

			# Decode and parse the message
			try:

				# Decode Message
				Message = json.loads(Consumer_Message.value().decode('utf-8'))

			# Check for JSON Decode Error
			except json.JSONDecodeError as e:

				# Log Error
				Log.Terminal_Log('ERROR', f'JSON Decode Error: {e}')

				# Continue
				continue

			# Get Data Packs
			Device = Message.get('Device', {})
			Power_Pack = Device.get('Power', {})
			IoT_Pack = Device.get('IoT', {})
			Payload = Message.get('Payload', {})

			# Define DB
			DB_Module = Database.SessionLocal()

			# Get Pack Dictionary
			try:
				
				# Query all data types
				Data_Type_Query = DB_Module.query(Models.Variable).all()

				# Get Data Type List
				Formatted_Data = [(Variable.Variable_ID, Variable.Variable_Unit) for Variable in Data_Type_Query]

			# Check for Error
			finally:

				# Close Database
				DB_Module.close()

			# Define Found Variables
			Found_Variables = {}

			# Check for Tuple and Extract Variable IDs
			keys_to_check = [var[0] if isinstance(var, tuple) else var for var in Formatted_Data]

			# Function to check variables in a given pack
			def Check_Variables_in_Pack(pack, pack_name):

				# Check for Pack
				for variable in keys_to_check:

					# Check for Variable
					if variable in pack:

						# Get Value
						value = pack[variable]

						# Check for Value
						if value is not None and value != "":

							# Add to Found Variables
							Found_Variables[variable] = value

			# Check for variables in Payload, Power_Pack, and IoT_Pack
			Check_Variables_in_Pack(Power_Pack, 'Power_Pack')
			Check_Variables_in_Pack(IoT_Pack, 'IoT_Pack')
			Check_Variables_in_Pack(Payload, 'Payload')

			evaluate_composite_rules(Found_Variables)

			# Log Found Variables
#			Log.Terminal_Log('INFO', f'Found Variables: {Found_Variables}')
			Log.Terminal_Log('INFO', '-------------------------------------------------------------')














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
