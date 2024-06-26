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

	ops = {
		'>': operator.gt,
		'<': operator.lt,
		'>=': operator.ge,
		'<=': operator.le,
		'==': operator.eq,
		'!=': operator.ne
	}

	for op_str, op_func in ops.items():
		if op_str in condition:
			cond_value = float(condition.split(op_str)[-1].strip())
			return op_func(value, cond_value)
	return False

def evaluate_composite_rules(device_id, data):

	with Database.SessionLocal() as session:
		main_rules = session.query(Models.Rules).all()
		
		for main_rule in main_rules:
			rule_id = main_rule.Rule_ID
			action = main_rule.Rule_Action_ID
			
			sub_rules = session.query(Models.Rule_Chain).filter(Models.Rule_Chain.Rule_ID == rule_id).all()
			
			all_conditions_met = True
			for sub_rule in sub_rules:
				rule_device_id, variable_id, condition = sub_rule.Device_ID, sub_rule.Variable_ID, sub_rule.Rule_Condition
				if rule_device_id == device_id and variable_id in data:
					value = data[variable_id]
					if not evaluate_condition(value, condition):
						all_conditions_met = False
						break
				else:
					all_conditions_met = False
					break
			
			if all_conditions_met:
				Log.Terminal_Log('INFO', f'Rule Action: {action}')











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

			Headers = {key: value.decode('utf-8') for key, value in Consumer_Message.headers()}

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

			evaluate_composite_rules(Headers['Device_ID'], Found_Variables)

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
