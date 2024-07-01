# Setup Root Path
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Library Includes
from Setup.Config import APP_Settings
from Setup import Models, Database
from Functions import Log
import pandas as pd
import time

# Define Github Repository
Github_Repository = "https://raw.githubusercontent.com/akkoyun/Standartlar/main/PostOffice/Data"

# Read CSV From Github
def Read_CSV_From_Github(File_Name):

	# Define URL
	URL = f"{Github_Repository}/{File_Name}"

	# Download Data File
	try:
		
		# Download Data File
		Data_File = pd.read_csv(URL)

	except Exception as e:

		# Log Message
		Log.Terminal_Log("ERROR", f"Data file read error: {e}")

	# Wait for 1 Second
	time.sleep(1)

	# Return Data File
	return Data_File

# Import Data_Segment Data
def Import_Data_Segment():

	# New Data Count Definition
	New_Data_Count = 0

	# Define Data File
	Data_File = Read_CSV_From_Github(APP_Settings.FILE_DATA_SEGMENT)

	# Rename Columns
	Data_File.columns = ['Segment_ID', 'Segment_Name', 'Description']

	# Define DB
	with Database.DB_Session_Scope() as DB:

		# Add Record to DataBase
		for index, row in Data_File.iterrows():

			# Check for Existing
			Query = DB.query(Models.Data_Segment).filter(
				Models.Data_Segment.Segment_Name == str(row['Segment_Name'])
			).first()

			# Record Not Found
			if not Query:

				# Create New Record
				New_Record = Models.Data_Segment(
					Segment_ID=int(row['Segment_ID']),
					Segment_Name=str(row['Segment_Name']),
					Description=str(row['Description'])
				)

				# Add Record to DataBase
				try:

					# Add Record to DataBase
					DB.add(New_Record)

					# Commit DataBase
					DB.commit()

					# Increase New Count
					New_Data_Count += 1

				except Exception as e:

					# Rollback in case of error
					DB.rollback()

	# Log the result
	if New_Data_Count > 0:

		# Log the result
		Log.Terminal_Log("INFO", f"[{New_Data_Count}] New Data Segment Added.")

	# Up to Date
	else:

		# Log the result
		Log.Terminal_Log("INFO", f"Data Segment is up to date.")

# Import Command Data
def Import_Command():

	# New Calibration Count Definition
	New_Data_Count = 0

	# Define Data File
	Data_File = Read_CSV_From_Github(APP_Settings.FILE_COMMAND)

	# Rename Columns
	Data_File.columns = ['Command_ID', 'Command', 'Description']

	# Define DB
	with Database.DB_Session_Scope() as DB:

		# Add Record to DataBase
		for index, row in Data_File.iterrows():

			# Check for Existing
			Query = DB.query(Models.Command).filter(
				Models.Command.Command==str(row['Command'])
			).first()

			# Record Not Found
			if not Query:

				# Create New Record
				New_Record = Models.Command(
					Command_ID=int(row['Command_ID']),
					Command=str(row['Command']),
					Description=str(row['Description'])
				)

				# Add Record to DataBase
				try:

					# Add Record to DataBase
					DB.add(New_Record)

					# Commit DataBase
					DB.commit()

					# Increase New Count
					New_Data_Count += 1

				except Exception as e:

					# Rollback in case of error
					DB.rollback()

	# Log the result
	if New_Data_Count > 0:

		# Log the result
		Log.Terminal_Log("INFO", f"[{New_Data_Count}] New Command Added.")

	# Up to Date
	else:

		# Log the result
		Log.Terminal_Log("INFO", f"Command is up to date.")

# Import Data_Type Data
def Import_Data_Type():

	# New Data Count Definition
	New_Data_Count = 0

	# Define Data File
	Data_File = Read_CSV_From_Github(APP_Settings.FILE_MEASUREMENT_TYPE)

	# Rename Columns
	Data_File.columns = ['Variable_ID', 'Variable_Description', 'Variable_Unit', 'Segment_ID']

	# Define DB
	with Database.DB_Session_Scope() as DB:

		# Iterate over each row in the CSV file
		for index, row in Data_File.iterrows():

			# Check if the record already exists
			Query = DB.query(Models.Variable).filter(
				Models.Variable.Variable_ID == str(row['Variable_ID'])
			).first()
			
			# If the record does not exist
			if not Query:

				# Create a new record
				New_Record = Models.Variable(
					Variable_ID=str(row['Variable_ID']),
					Variable_Description=str(row['Variable_Description']),
					Variable_Unit=str(row['Variable_Unit']),
					Segment_ID=int(row['Segment_ID'])
				)

				# Add Record to DataBase
				try:

					# Add Record to DataBase
					DB.add(New_Record)

					# Commit DataBase
					DB.commit()

					# Increase New Count
					New_Data_Count += 1

				except Exception as e:

					# Rollback in case of error
					DB.rollback()

	# Log the result
	if New_Data_Count > 0:

		# Log the result
		Log.Terminal_Log("INFO", f"[{New_Data_Count}] New Data_Type Added.")

	else:

		# Log the result
		Log.Terminal_Log("INFO", f"Data_Type is up to date.")

# Import GSM Operator Data
def Import_GSM_Operator():

	# New Data Count Definition
	New_Data_Count = 0

	# Define Data File
	Data_File = Read_CSV_From_Github(APP_Settings.FILE_GSM_OPERATOR)

	# Rename Columns
	Data_File.columns = ['MCC_ID', 'MCC_ISO', 'MCC_Country_Name', 'MCC_Country_Code', 'MCC_Country_Flag_Image_URL', 'MNC_ID', 'MNC_Brand_Name', 'MNC_Operator_Name', 'MNC_Operator_Image_URL']

	# Define DB
	with Database.DB_Session_Scope() as DB:

		# Add Record to DataBase
		for index, row in Data_File.iterrows():

			# Check for Existing
			Query = DB.query(Models.GSM_Operator).filter(
				Models.GSM_Operator.MCC_ID == int(row['MCC_ID']), 
				Models.GSM_Operator.MNC_ID == int(row['MNC_ID'])
			).first()

			# Record Not Found
			if not Query:

				# Create New Record
				New_Record = Models.GSM_Operator(
					MCC_ID=int(row['MCC_ID']),
					MCC_ISO=str(row['MCC_ISO']),
					MCC_Country_Name=str(row['MCC_Country_Name']),
					MCC_Country_Code=int(row['MCC_Country_Code']) if not pd.isna(row['MCC_Country_Code']) else None,
					MCC_Country_Flag_Image_URL=str(row['MCC_Country_Flag_Image_URL']) if not pd.isna(row['MCC_Country_Flag_Image_URL']) else None,
					MNC_ID=int(row['MNC_ID']),
					MNC_Brand_Name=str(row['MNC_Brand_Name']),
					MNC_Operator_Name=str(row['MNC_Operator_Name']),
					MNC_Operator_Image_URL=str(row['MNC_Operator_Image_URL']) if not pd.isna(row['MNC_Operator_Image_URL']) else None,
				)

				# Add Record to DataBase
				try:

					# Add Record to DataBase
					DB.add(New_Record)

					# Commit DataBase
					DB.commit()

					# Increase New Count
					New_Data_Count += 1

				except Exception as e:

					# Rollback in case of error
					DB.rollback()

	# Log the result
	if New_Data_Count > 0:

		# Log the result
		Log.Terminal_Log("INFO", f"[{New_Data_Count}] New GSM Operator Added.")

	else:

		# Log the result
		Log.Terminal_Log("INFO", f"GSM Operator is up to date.")

# Import Status Data
def Import_Status():

	# New Data Count Definition
	New_Data_Count = 0

	# Define Data File
	Data_File = Read_CSV_From_Github(APP_Settings.FILE_STATUS)

	# Rename Columns
	Data_File.columns = ['Status_ID', 'Description']

	# Define DB
	with Database.DB_Session_Scope() as DB:

		# Add Record to DataBase
		for index, row in Data_File.iterrows():

			# Check for Existing
			Query = DB.query(Models.Status).filter(
				Models.Status.Description.like(str(row['Description']))
			).first()

			# Record Not Found
			if not Query:

				# Create New Record
				New_Record = Models.Status(
					Status_ID=int(row['Status_ID']),
					Description=str(row['Description']),
				)

				# Add Record to DataBase
				try:

					# Add Record to DataBase
					DB.add(New_Record)

					# Commit DataBase
					DB.commit()

					# Increase New Count
					New_Data_Count += 1

				except Exception as e:

					# Rollback in case of error
					DB.rollback()

	# Log the result
	if New_Data_Count > 0:

		# Log the result
		Log.Terminal_Log("INFO", f"[{New_Data_Count}] New Status Added.")

	else:

		# Log the result
		Log.Terminal_Log("INFO", f"Status is up to date.")

# Import Version Data
def Import_Version():

	# New Data Count Definition
	New_Data_Count = 0

	# Define Data File
	Data_File = Read_CSV_From_Github(APP_Settings.FILE_VERSION)

	# Rename Columns
	Data_File.columns = ['Version_ID', 'Firmware']

	# Define DB
	with Database.DB_Session_Scope() as DB:

		# Add Record to DataBase
		for index, row in Data_File.iterrows():

			# Check for Existing
			Query = DB.query(Models.Version).filter(
				Models.Version.Firmware.like(str(row['Firmware']))
			).first()

			# Record Not Found
			if not Query:

				# Create New Record
				New_Record = Models.Version(
					Version_ID=int(row['Version_ID']),
					Firmware=str(row['Firmware']),
				)

				# Add Record to DataBase
				try:

					# Add Record to DataBase
					DB.add(New_Record)

					# Commit DataBase
					DB.commit()

					# Increase New Count
					New_Data_Count += 1

				except Exception as e:

					# Rollback in case of error
					DB.rollback()

	# Log the result
	if New_Data_Count > 0:

		# Log the result
		Log.Terminal_Log("INFO", f"[{New_Data_Count}] New Version Added.")

	else:

		# Log the result
		Log.Terminal_Log("INFO", f"Version is up to date.")

# Import Model Data
def Import_Model():

	# New Data Count Definition
	New_Data_Count = 0

	# Define Data File
	Data_File = Read_CSV_From_Github(APP_Settings.FILE_MODEL)

	# Rename Columns
	Data_File.columns = ['Model_ID', 'Model_Name', 'Model_Description']

	# Define DB
	with Database.DB_Session_Scope() as DB:

		# Add Record to DataBase
		for index, row in Data_File.iterrows():

			# Check for Existing
			Query = DB.query(Models.Model).filter(
				Models.Model.Model_Name.like(str(row['Model_Name']))
			).first()

			# Record Not Found
			if not Query:

				# Create New Record
				New_Record = Models.Model(
					Model_ID=int(row['Model_ID']),
					Model_Name=str(row['Model_Name']),
					Model_Description=str(row['Model_Description'])
				)

				# Add Record to DataBase
				try:

					# Add Record to DataBase
					DB.add(New_Record)

					# Commit DataBase
					DB.commit()

					# Increase New Count
					New_Data_Count += 1

				except Exception as e:

					# Rollback in case of error
					DB.rollback()

	# Log the result
	if New_Data_Count > 0:

		# Log the result
		Log.Terminal_Log("INFO", f"[{New_Data_Count}] New Model Added.")

	else:

		# Log the result
		Log.Terminal_Log("INFO", f"Model is up to date.")	

# Import Modem Data
def Import_Modem():

	# New Data Count Definition
	New_Data_Count = 0

	# Define Data File
	Data_File = Read_CSV_From_Github(APP_Settings.FILE_MODEM)

	# Rename Columns
	Data_File.columns = ['IMEI', 'Model_ID', 'Manufacturer_ID']

	# Define DB
	with Database.DB_Session_Scope() as DB:

		# Add Record to DataBase
		for index, row in Data_File.iterrows():

			# Check for Existing
			Query = DB.query(Models.Modem).filter(
				Models.Modem.IMEI.like(str(row['IMEI']))
			).first()

			# Record Not Found
			if not Query:

				# Create New Record
				New_Record = Models.Modem(
					IMEI=str(row['IMEI']),
					Model_ID=int(row['Model_ID']),
					Manufacturer_ID=int(row['Manufacturer_ID']),
				)

				# Add Record to DataBase
				try:

					# Add Record to DataBase
					DB.add(New_Record)

					# Commit DataBase
					DB.commit()

					# Increase New Count
					New_Data_Count += 1

				except Exception as e:

					# Rollback in case of error
					DB.rollback()

	# Log the result
	if New_Data_Count > 0:

		# Log the result
		Log.Terminal_Log("INFO", f"[{New_Data_Count}] New Modem Added.")

	else:

		# Log the result
		Log.Terminal_Log("INFO", f"Modem is up to date.")

# Import Project Data
def Import_Project():

	# New Data Count Definition
	New_Data_Count = 0

	# Define Data File
	Data_File = Read_CSV_From_Github(APP_Settings.FILE_PROJECT)

	# Rename Columns
	Data_File.columns = ['Project_ID', 'Project_Name']

	# Define DB
	with Database.DB_Session_Scope() as DB:

		# Add Record to DataBase
		for index, row in Data_File.iterrows():

			# Check for Existing
			Query = DB.query(Models.Project).filter(
				Models.Project.Project_Name.like(str(row['Project_Name']))
			).first()

			# Record Not Found
			if not Query:

				# Create New Record
				New_Record = Models.Project(
					Project_ID=int(row['Project_ID']),
					Project_Name=str(row['Project_Name'])
				)

				# Add Record to DataBase
				try:

					# Add Record to DataBase
					DB.add(New_Record)

					# Commit DataBase
					DB.commit()

					# Increase New Count
					New_Data_Count += 1

				except Exception as e:

					# Rollback in case of error
					DB.rollback()

	# Log the result
	if New_Data_Count > 0:

		# Log the result
		Log.Terminal_Log("INFO", f"[{New_Data_Count}] New Project Added.")

	else:

		# Log the result
		Log.Terminal_Log("INFO", f"Project is up to date.")

# Import Device Data
def Import_Device():

	# New Data Count Definition
	New_Data_Count = 0

	# Define Data File
	Data_File = Read_CSV_From_Github(APP_Settings.FILE_DEVICE)

	# Rename Columns
	Data_File.columns = ['Device_ID', 'Status_ID', 'Version_ID', 'Model_ID', 'IMEI', 'Project_ID']

	# Define DB
	with Database.DB_Session_Scope() as DB:

		# Add Record to DataBase
		for index, row in Data_File.iterrows():

			# Check for Existing
			Query = DB.query(Models.Device).filter(
				Models.Device.Device_ID.like(str(row['Device_ID']))
			).first()

			# Record Not Found
			if not Query:

				# Create New Record
				New_Record = Models.Device(
					Device_ID=str(row['Device_ID']),
					Status_ID=int(row['Status_ID']),
					Version_ID=int(row['Version_ID']),
					Project_ID=int(row['Project_ID']),
					Model_ID=int(row['Model_ID']),
					Manufacturer_ID=0,
					IMEI=str(row['IMEI'])
				)

				# Add Record to DataBase
				try:

					# Add Record to DataBase
					DB.add(New_Record)

					# Commit DataBase
					DB.commit()

					# Increase New Count
					New_Data_Count += 1

				except Exception as e:

					# Rollback in case of error
					DB.rollback()

	# Log the result
	if New_Data_Count > 0:

		# Log the result
		Log.Terminal_Log("INFO", f"[{New_Data_Count}] New Device Added.")

	else:

		# Log the result
		Log.Terminal_Log("INFO", f"Device is up to date.")

# Import SIM Data
def Import_SIM():

	# New Data Count Definition
	New_Data_Count = 0

	# Define Data File
	Data_File = Read_CSV_From_Github(APP_Settings.FILE_SIM)

	# Rename Columns
	Data_File.columns = ['SIM_ICCID', 'MCC_ID', 'MNC_ID', 'SIM_Number']

	# Define DB
	with Database.DB_Session_Scope() as DB:

		# Add Record to DataBase
		for index, row in Data_File.iterrows():

			# Check for Existing
			Query = DB.query(Models.SIM).filter(
				Models.SIM.ICCID.like(str(row['SIM_ICCID']))
			).first()

			# Record Not Found
			if not Query:

				# Create New Record
				New_Record = Models.SIM(
					ICCID=str(row['SIM_ICCID']),
					Operator_ID=int(row['MCC_ID']),
					GSM_Number=str(row['SIM_Number'])
				)

				# Add Record to DataBase
				try:

					# Add Record to DataBase
					DB.add(New_Record)

					# Commit DataBase
					DB.commit()

					# Increase New Count
					New_Data_Count += 1

				except Exception as e:

					# Rollback in case of error
					DB.rollback()

	# Log the result
	if New_Data_Count > 0:

		# Log the result
		Log.Terminal_Log("INFO", f"[{New_Data_Count}] New SIM Added.")

	else:

		# Log the result
		Log.Terminal_Log("INFO", f"SIM is up to date.")

# Import Calibration Data
def Import_Calibration():

	# New Calibration Count Definition
	Existing_Data_Count = 0
	New_Data_Count = 0

	# Define Data File
	Data_File = Read_CSV_From_Github(APP_Settings.FILE_CALIBRATION)

	# Rename Columns
	Data_File.columns = ['Calibration_ID', 'Device_ID', 'Variable_ID', 'Gain', 'Offset']

	# Define DB
	with Database.DB_Session_Scope() as DB:

		# Add Record to DataBase
		for index, row in Data_File.iterrows():

			# Check for Existing
			Query = DB.query(Models.Calibration).filter(
				Models.Calibration.Device_ID.like(str(row['Device_ID'])),
				Models.Calibration.Variable_ID.like(str(row['Variable_ID']))
			).first()

			# Record Not Found
			if not Query:

				# Create New Record
				New_Record = Models.Calibration(
					Calibration_ID=int(row['Calibration_ID']),
					Device_ID=str(row['Device_ID']),
					Variable_ID=str(row['Variable_ID']),
					Gain=float(row['Gain']),
					Offset=float(row['Offset']),
				)

				# Add Record to DataBase
				try:

					# Add Record to DataBase
					DB.add(New_Record)

					# Commit DataBase
					DB.commit()

					# Increase New Count
					New_Data_Count += 1

				except Exception as e:

					# Rollback in case of error
					DB.rollback()

			# Record Found
			else:

				# Increase Existing Count
				Existing_Data_Count += 1

	# Log the result
	if New_Data_Count > 0:

		# Log the result
		Log.Terminal_Log("INFO", f"[{New_Data_Count}] New Calibration Added [{Existing_Data_Count}].")

	else:

		# Log the result
		Log.Terminal_Log("INFO", f"Calibration is up to date [{Existing_Data_Count}].")

# Import Manufacturer Data
def Import_Manufacturer():

	# New Data Count Definition
	New_Data_Count = 0

	# Define Data File
	Data_File = Read_CSV_From_Github(APP_Settings.FILE_MANUFACTURER)

	# Rename Columns
	Data_File.columns = ['Manufacturer_ID', 'Manufacturer']

	# Define DB
	with Database.DB_Session_Scope() as DB:

		# Add Record to DataBase
		for index, row in Data_File.iterrows():

			# Check for Existing
			Query = DB.query(Models.Manufacturer).filter(
				Models.Manufacturer.Manufacturer_Name.like(str(row['Manufacturer']))
			).first()

			# Record Not Found
			if not Query:

				# Create New Record
				New_Record = Models.Manufacturer(
					Manufacturer_ID=int(row['Manufacturer_ID']),
					Manufacturer_Name=str(row['Manufacturer']),
				)

				# Add Record to DataBase
				try:

					# Add Record to DataBase
					DB.add(New_Record)

					# Commit DataBase
					DB.commit()

					# Increase New Count
					New_Data_Count += 1

				except Exception as e:

					# Rollback in case of error
					DB.rollback()

	# Log the result
	if New_Data_Count > 0:

		# Log the result
		Log.Terminal_Log("INFO", f"[{New_Data_Count}] New Manufacturer Added.")

	else:

		# Log the result
		Log.Terminal_Log("INFO", f"Manufacturer is up to date.")

# Import Connection Data
def Import_Connection():

	# New Calibration Count Definition
	New_Data_Count = 0

	# Define Data File
	Data_File = Read_CSV_From_Github(APP_Settings.FILE_CONNECTION)

	# Rename Columns
	Data_File.columns = ['IP_Address', 'IP_Pool']

	# Define DB
	with Database.DB_Session_Scope() as DB:

		# Add Record to DataBase
		for index, row in Data_File.iterrows():

			# Check for Existing
			Query = DB.query(Models.Connection).filter(
				Models.Connection.IP_Address==str(row['IP_Address'])
			).first()

			# Record Not Found
			if not Query:

				# Create New Record
				New_Record = Models.Connection(
					IP_Address=str(row['IP_Address']),
					IP_Pool=bool(row['IP_Pool'])
				)

				# Add Record to DataBase
				try:

					# Add Record to DataBase
					DB.add(New_Record)

					# Commit DataBase
					DB.commit()

					# Increase New Count
					New_Data_Count += 1

				except Exception as e:

					# Rollback in case of error
					DB.rollback()

	# Log the result
	if New_Data_Count > 0:

		# Log the result
		Log.Terminal_Log("INFO", f"[{New_Data_Count}] New IP Addres Added.")

	else:

		# Log the result
		Log.Terminal_Log("INFO", f"IP address is up to date.")

# Create Tables
Database.Base.metadata.create_all(bind=Database.DB_Engine)

# Update Tables
Import_Status()
Import_Version()
Import_Project()
Import_Model()
Import_Manufacturer()
Import_Modem()
Import_GSM_Operator()
Import_SIM()
Import_Connection()
Import_Command()
Import_Data_Segment()
Import_Data_Type()
Import_Calibration()
Import_Device()
