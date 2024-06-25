# Setup Library
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Import Libraries
from Setup import Schema, Definitions, Config
from Functions import Log, Database_Functions, ICCID_Functions
from confluent_kafka import Consumer, KafkaError
from pydantic import ValidationError
import time, json

# Define Kafka Consumer
Consumer_Config = {
    'bootstrap.servers': f'{Config.APP_Settings.KAFKA_HOSTNAME}:{Config.APP_Settings.KAFKA_PORT}',
    'group.id': 'RAW_Handler_Group',
    'auto.offset.reset': 'earliest',
	'enable.auto.commit': False,
}

# Define Consumer Class
RAW_Consumer = Consumer(Consumer_Config)

# Define Subscription Function
RAW_Consumer.subscribe([Config.APP_Settings.KAFKA_RAW_TOPIC])

# Define Consumer Topic Loop
try:

	while True:

		# Get Message
		Consumer_Message = RAW_Consumer.poll(timeout=1.0)

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

			# Define Variables
			Stream_Data = Definitions.StreamData()

			# Get Headers
			Headers = {key: value.decode('utf-8') for key, value in Consumer_Message.headers()}

			# Get Message
			try:

				# Decode Message
				RAW_Message = Consumer_Message.value().decode('utf-8')

				# Check if RAW_Message is valid
				if not RAW_Message:

					# Continue
					continue

				# Parse RAW_Message to dict if it's a JSON string
				if isinstance(RAW_Message, str):

					# Parse RAW_Message
					try:

						# Parse RAW_Message
						RAW_Message = json.loads(RAW_Message)

					# Check for JSONDecodeError
					except json.JSONDecodeError as e:

						# Continue
						continue

				# Ensure RAW_Message is a dict
				if not isinstance(RAW_Message, dict):

					# Continue
					continue

				# Parse Message using Schema
				Stream_Data.message = Schema.Data_Pack(**RAW_Message)

			# Check for Errors
			except (TypeError, json.JSONDecodeError, ValidationError) as e:

				# Continue
				continue

			# Get Command ID
			Stream_Data.command_id = Database_Functions.Get_Command_ID(
				Headers['Command']
			)

			# Get or Create Device Firmware
			Stream_Data.device_firmware_id = Database_Functions.Get_or_Create_Firmware(
				Stream_Data.message.Info.Firmware
			)

			# Check for SIM
			Stream_Data.iccid = ICCID_Functions.Verify_and_Strip_ICCID(
				Stream_Data.message.Info.ICCID
			)

			# Get or Create SIM Existence
			Stream_Data.sim_id = Database_Functions.Get_or_Create_SIM(
				Stream_Data.message.Info.ICCID,
				Stream_Data.message.Device.IoT.MCC,
				Stream_Data.message.Device.IoT.MNC
			)

			# Check for Modem
			Stream_Data.new_modem = Database_Functions.Get_or_Create_Modem(
				Stream_Data.message.Info.IMEI
			)

			# Check for Device
			Stream_Data.new_device = Database_Functions.Get_or_Create_Device(
				Stream_Data.message.Info.ID,
				Stream_Data.device_firmware_id,
				Stream_Data.message.Info.IMEI,
				Headers['Device_IP'],
				Headers['Device_Time']
			)

			# Check for Connection Table
			Stream_Data.new_connection = Database_Functions.Get_or_Create_Connection(
				Headers['Device_IP']
			)

			# Create Stream
			Stream_Data.stream_id = Database_Functions.Create_Stream(
				Stream_Data, 
				Headers
			)

			# Log Message
			Log.Terminal_Log('INFO', f'Stream ID   : {Stream_Data.stream_id} - {Headers["Command"]}')
			Log.Terminal_Log('INFO', f'Device ID   : {Stream_Data.message.Info.ID} - {Stream_Data.message.Info.Firmware} - {Stream_Data.new_device}')
			Log.Terminal_Log('INFO', f'ICCID       : {Stream_Data.iccid} - {Stream_Data.sim_id}')
			Log.Terminal_Log('INFO', f'IMEI        : {Stream_Data.message.Info.IMEI} - {Stream_Data.new_modem}')

			# Define Record Count
			Power_Record_Count = 0
			IoT_Record_Count = 0
			Payload_Record_Count = 0
			
			# Record Power Measurements
			Power_Record_Count = Database_Functions.Record_Measurement(Stream_Data.message.Device.Power, Stream_Data.stream_id, Definitions.Variable_Segment.Power.value)

			# Record IoT Measurements
			IoT_Record_Count = Database_Functions.Record_Measurement(Stream_Data.message.Device.IoT, Stream_Data.stream_id, Definitions.Variable_Segment.GSM.value)

			# Record Payload Measurements
			Payload_Record_Count += Database_Functions.Record_Measurement(Stream_Data.message.Payload, Stream_Data.stream_id, Definitions.Variable_Segment.Device.value)
			Payload_Record_Count += Database_Functions.Record_Measurement(Stream_Data.message.Payload, Stream_Data.stream_id, Definitions.Variable_Segment.Location.value)
			Payload_Record_Count += Database_Functions.Record_Measurement(Stream_Data.message.Payload, Stream_Data.stream_id, Definitions.Variable_Segment.Environment.value)
			Payload_Record_Count += Database_Functions.Record_Measurement(Stream_Data.message.Payload, Stream_Data.stream_id, Definitions.Variable_Segment.Water.value)
			Payload_Record_Count += Database_Functions.Record_Measurement(Stream_Data.message.Payload, Stream_Data.stream_id, Definitions.Variable_Segment.Energy.value)
			Payload_Record_Count += Database_Functions.Record_Measurement(Stream_Data.message.Payload, Stream_Data.stream_id, Definitions.Variable_Segment.FOTA.value)

			# Log Message
			Log.Terminal_Log('INFO', f'New Power   : {Power_Record_Count}')
			Log.Terminal_Log('INFO', f'New IoT     : {IoT_Record_Count}')
			Log.Terminal_Log('INFO', f'New Payload : {Payload_Record_Count}')
			Log.Terminal_Log('INFO', f'-------------------------------------------------------------')

			# Commit Message
			RAW_Consumer.commit(asynchronous=False)

except KeyboardInterrupt:

	# Consumer Closed Manually
    Log.Terminal_Log('INFO', 'Handler is shutting down...')

finally:

	# Wait for Finish
	time.sleep(2)

	# Close Consumer
	RAW_Consumer.close()
