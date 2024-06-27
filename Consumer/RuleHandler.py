# Setup Library
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Import Libraries
from Setup import Config, Database, Models
from Functions import Log
from confluent_kafka import Consumer, KafkaError
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

# Function to evaluate a single rule
def Evaluate_Condition(value, condition):

    # Define Operators
    Operators = {
        '>': operator.gt,
        '<': operator.lt,
        '>=': operator.ge,
        '<=': operator.le,
        '==': operator.eq,
        '!=': operator.ne
    }

    # Check for Condition
    for Operator_String, Operator_Function in Operators.items():

		# Check for Operator
        if Operator_String in condition:

            # Check for Value
            Condition_Value = float(condition.split(Operator_String)[-1].strip())

            # Return Result
            return Operator_Function(value, Condition_Value)

    # Return False
    return False

# Function to evaluate composite rules
def Evaluate_Composite_Rules(device_id, data, triggered_rules):

    # Define Action
    with Database.SessionLocal() as session:

        # Get all main rules
        Rules = session.query(Models.Rules).all()

        # Check for Rules
        for Rule in Rules:

            # Get Rule ID and Action
            Rule_ID = Rule.Rule_ID
            Rule_Action = Rule.Rule_Action_ID
            Rule_Status = Rule.Rule_Status

            # Get all sub rules
            Rule_Chains = session.query(Models.Rule_Chain).filter(Models.Rule_Chain.Rule_ID == Rule_ID).all()

            # Define All Conditions Met
            All_Conditions_Met = True

            # Check for Rule Chains
            for Rule_Chain in Rule_Chains:

                # Get Rule Chain Data
                Rule_Device_ID, Rule_Variable_ID, Rule_Condition = Rule_Chain.Device_ID, Rule_Chain.Variable_ID, Rule_Chain.Rule_Condition

                # Check for Device ID and Variable ID
                if Rule_Device_ID == device_id and Rule_Status == True and Rule_Variable_ID in data:

                    # Get Value
                    Value = data[Rule_Variable_ID]

                    # Evaluate Condition
                    if not Evaluate_Condition(Value, Rule_Condition):

                        # Condition Not Met
                        All_Conditions_Met = False
                        break

                else:

                    # Condition Not Met
                    All_Conditions_Met = False
                    break

            # Check for All Conditions Met
            if All_Conditions_Met:

                # Get Rule for Update
                Rule_Update = session.query(Models.Rules).filter(Models.Rules.Rule_ID == Rule_ID).first()

                # Update Rule
                Rule_Update.Rule_Trigger_Count += 1

                # Commit Update
                session.commit()

                # Log Rule Triggered
                Log.Terminal_Log('INFO', f'Rule --> [{device_id}] - [Rule ID: {Rule_ID}] - Action Triggered')

				# Append Triggered Rule
                triggered_rules.append((device_id, Rule_ID, Rule_Action))

# Define Consumer Topic Loop
try:

    while True:

        # Get Message
        Consumer_Message = Rule_Consumer.poll(timeout=1.0)

        # Check for Message
        if Consumer_Message is None:
            continue

        # Check for Error
        if Consumer_Message.error():
            if Consumer_Message.error().code() == KafkaError._PARTITION_EOF:
                continue
            elif Consumer_Message.error():
                Log.Terminal_Log('ERROR', f'Consumer Error: {Consumer_Message.error()}')
            continue

        else:

			# Check for Message Value
            try:

                # Decode Message
                Message = json.loads(Consumer_Message.value().decode('utf-8'))

			# Check for JSON Decode Error
            except json.JSONDecodeError as e:

				# Log Error
                Log.Terminal_Log('ERROR', f'JSON Decode Error: {e}')

				# Continue
                continue

            # Get Headers
            Headers = {key: value.decode('utf-8') for key, value in Consumer_Message.headers()}

            # Get Data Packs
            Device = Message.get('Device', {})
            Power_Pack = Device.get('Power', {})
            IoT_Pack = Device.get('IoT', {})
            Payload = Message.get('Payload', {})

            # Define DB
            DB_Module = Database.SessionLocal()

			# Get Data Types
            try:

				# Get Data Types
                Data_Type_Query = DB_Module.query(Models.Variable).all()

				# Format Data
                Formatted_Data = [(Variable.Variable_ID, Variable.Variable_Unit) for Variable in Data_Type_Query]

            finally:

				# Close DB
                DB_Module.close()

            # Define Found Variables
            Found_Variables = {}

            # Define Rule Action
            Action = 0

            # Check for Tuple and Extract Variable IDs
            keys_to_check = [var[0] if isinstance(var, tuple) else var for var in Formatted_Data]

            # Function to check variables in a given pack
            def Check_Variables_in_Pack(pack, pack_name):
                for variable in keys_to_check:
                    if variable in pack:
                        value = pack[variable]
                        if value is not None and value != "":
                            Found_Variables[variable] = value

			# Check Variables in Packs
            Check_Variables_in_Pack(Power_Pack, 'Power_Pack')
            Check_Variables_in_Pack(IoT_Pack, 'IoT_Pack')
            Check_Variables_in_Pack(Payload, 'Payload')

            # Define Triggered Rules
            Triggered_Rules = []

			# Evaluate Composite Rules
            Evaluate_Composite_Rules(Headers['Device_ID'], Found_Variables, Triggered_Rules)

            # Log Found Variables
            if not Triggered_Rules:

				# Log No Action
                Log.Terminal_Log('INFO', f'Rule --> [{Headers["Device_ID"]}] - No Action')

            else:

				# Log Triggered Rules
                for device_id, rule_id, action in Triggered_Rules:

					# Log Action
                    Log.Terminal_Log('INFO', f'Rule --> [{device_id}] - Rule ID: {rule_id} - Action Triggered: {action}')

            # Commit Message
            Rule_Consumer.commit(asynchronous=False)

# Handle Keyboard Interrupt
except KeyboardInterrupt:

	# Log Shutdown
    Log.Terminal_Log('INFO', 'Handler is shutting down...')

# Handle Finally
finally:

	# Close Consumer
    time.sleep(2)

	# Log Shutdown
    Rule_Consumer.close()
