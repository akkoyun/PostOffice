# Setup Root Path
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup.Config import APP_Settings
from Setup import Models, Database
from Functions import Log
import pandas as pd

# Import Data_Segment Data
def Import_Data_Segment():

    # New Data Count Definition
    New_Data_Count = 0

    # Define Data File
    Data_File_Name = APP_Settings.DATA_REPOSITORY + APP_Settings.FILE_DATA_SEGMENT

    # Download Data File
    try:
        
        # Download Data File
        Data_File = pd.read_csv(Data_File_Name)

    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"Data file read error.")

        # Exit
        exit()

    # Rename Columns
    Data_File.columns = ['Segment_ID', 'Description']

    # Define DB
    with Database.DB_Session_Scope() as DB_Module:

        # Add Record to DataBase
        for index, row in Data_File.iterrows():

            # Check for Existing
            Query = DB_Module.query(Models.Data_Segment).filter(Models.Data_Segment.Description.like(str(row['Description']))).first()

            # Record Not Found
            if not Query:

                # Create New Record
                New_Record = Models.Data_Segment(
                    Segment_ID=int(row['Segment_ID']),
                    Description=str(row['Description']),
                )

                # Add Record to DataBase
                try:
                
                    # Add Record to DataBase
                    DB_Module.add(New_Record)

                    # Increase New Count
                    New_Data_Count += 1

                except Exception as e:

                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding Device: {e}")

    # End Function
    return New_Data_Count

# Import Operator Data
def Import_GSM_Operator():

    # New Data Count Definition
    New_Data_Count = 0

    # Define Data File
    Data_File_Name = APP_Settings.DATA_REPOSITORY + APP_Settings.FILE_GSM_OPERATOR

    # Download Data File
    try:
        
        # Download Data File
        Data_File = pd.read_csv(Data_File_Name)

    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"Data file read error.")

        # Exit
        exit()

    # Rename Columns
    Data_File.columns = ['MCC_ID', 'MCC_ISO', 'MCC_Country_Name', 'MCC_Country_Code', 'MCC_Country_Flag_Image_URL', 'MNC_ID', 'MNC_Brand_Name', 'MNC_Operator_Name', 'MNC_Operator_Image_URL']

    # Define DB
    with Database.DB_Session_Scope() as DB_Module:

        # Add Record to DataBase
        for index, row in Data_File.iterrows():

            # Check for Existing
            Query = DB_Module.query(Models.GSM_Operator).filter(Models.GSM_Operator.MCC_ID==int(row['MCC_ID'])).filter(Models.GSM_Operator.MNC_ID==int(row['MNC_ID'])).first()

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
                    DB_Module.add(New_Record)

                    # Increase New Count
                    New_Data_Count += 1

                except Exception as e:

                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding Device: {e}")

    # End Function
    return New_Data_Count

# Import Status Data
def Import_Status():

    # New Data Count Definition
    New_Data_Count = 0

    # Define Data File
    Data_File_Name = APP_Settings.DATA_REPOSITORY + APP_Settings.FILE_STATUS

    # Download Data File
    try:
        
        # Download Data File
        Data_File = pd.read_csv(Data_File_Name)

    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"Data file read error.")

        # Exit
        exit()

    # Rename Columns
    Data_File.columns = ['Status_ID', 'Description']

    # Define DB
    with Database.DB_Session_Scope() as DB_Module:

        # Add Record to DataBase
        for index, row in Data_File.iterrows():

            # Check for Existing
            Query = DB_Module.query(Models.Status).filter(Models.Status.Description.like(str(row['Description']))).first()

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
                    DB_Module.add(New_Record)

                    # Increase New Count
                    New_Data_Count += 1

                except Exception as e:

                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding Device: {e}")

    # End Function
    return New_Data_Count

# Import Version Data
def Import_Version():

    # New Data Count Definition
    New_Data_Count = 0

    # Define Data File
    Data_File_Name = APP_Settings.DATA_REPOSITORY + APP_Settings.FILE_VERSION

    # Download Data File
    try:
        
        # Download Data File
        Data_File = pd.read_csv(Data_File_Name)

    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"Data file read error.")

        # Exit
        exit()

    # Rename Columns
    Data_File.columns = ['Version_ID', 'Firmware']

    # Define DB
    with Database.DB_Session_Scope() as DB_Module:

        # Add Record to DataBase
        for index, row in Data_File.iterrows():

            # Check for Existing
            Query = DB_Module.query(Models.Version).filter(Models.Version.Firmware.like(str(row['Firmware']))).first()

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
                    DB_Module.add(New_Record)

                    # Increase New Count
                    New_Data_Count += 1

                except Exception as e:

                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding Device: {e}")

    # End Function
    return New_Data_Count

# Import Model Data
def Import_Model():

    # New Data Count Definition
    New_Data_Count = 0

    # Define Data File
    Data_File_Name = APP_Settings.DATA_REPOSITORY + APP_Settings.FILE_MODEL

    # Download Data File
    try:
        
        # Download Data File
        Data_File = pd.read_csv(Data_File_Name)

    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"Data file read error.")

        # Exit
        exit()

    # Rename Columns
    Data_File.columns = ['Model_ID', 'Model']

    # Define DB
    with Database.DB_Session_Scope() as DB_Module:

        # Add Record to DataBase
        for index, row in Data_File.iterrows():

            # Check for Existing
            Query = DB_Module.query(Models.Model).filter(Models.Model.Model_Name.like(str(row['Model']))).first()

            # Record Not Found
            if not Query:

                # Create New Record
                New_Record = Models.Model(
                    Model_ID=int(row['Model_ID']),
                    Model_Name=str(row['Model']),
                )

                # Add Record to DataBase
                try:
                
                    # Add Record to DataBase
                    DB_Module.add(New_Record)

                    # Increase New Count
                    New_Data_Count += 1

                except Exception as e:

                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding Device: {e}")

    # End Function
    return New_Data_Count

# Import Manufacturer Data
def Import_Manufacturer():

    # New Data Count Definition
    New_Data_Count = 0

    # Define Data File
    Data_File_Name = APP_Settings.DATA_REPOSITORY + APP_Settings.FILE_MANUFACTURER

    # Download Data File
    try:
        
        # Download Data File
        Data_File = pd.read_csv(Data_File_Name)

    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"Data file read error.")

        # Exit
        exit()

    # Rename Columns
    Data_File.columns = ['Manufacturer_ID', 'Manufacturer']

    # Define DB
    with Database.DB_Session_Scope() as DB_Module:

        # Add Record to DataBase
        for index, row in Data_File.iterrows():

            # Check for Existing
            Query = DB_Module.query(Models.Manufacturer).filter(Models.Manufacturer.Manufacturer_Name.like(str(row['Manufacturer']))).first()

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
                    DB_Module.add(New_Record)

                    # Increase New Count
                    New_Data_Count += 1

                except Exception as e:

                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding Manufacturer: {e}")

    # End Function
    return New_Data_Count

# Import Modem Data
def Import_Modem():

    # New Data Count Definition
    New_Data_Count = 0

    # Define Data File
    Data_File_Name = APP_Settings.DATA_REPOSITORY + APP_Settings.FILE_MODEM

    # Download Data File
    try:
        
        # Download Data File
        Data_File = pd.read_csv(Data_File_Name)

    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"Data file read error.")

        # Exit
        exit()

    # Rename Columns
    Data_File.columns = ['IMEI', 'Model_ID', 'Manufacturer_ID']

    # Define DB
    with Database.DB_Session_Scope() as DB_Module:

        # Add Record to DataBase
        for index, row in Data_File.iterrows():

            # Check for Existing
            Query = DB_Module.query(Models.Modem).filter(Models.Modem.IMEI.like(str(row['IMEI']))).first()

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
                    DB_Module.add(New_Record)

                    # Increase New Count
                    New_Data_Count += 1

                except Exception as e:

                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding Modem: {e}")

    # End Function
    return New_Data_Count

# Import Device Data
def Import_Device():

    # New Data Count Definition
    New_Data_Count = 0

    # Define Data File
    Data_File_Name = APP_Settings.DATA_REPOSITORY + APP_Settings.FILE_DEVICE

    # Download Data File
    try:
        
        # Download Data File
        Data_File = pd.read_csv(Data_File_Name)

    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"Data file read error.")

        # Exit
        exit()

    # Rename Columns
    Data_File.columns = ['Device_ID', 'Status_ID', 'Version_ID', 'Model_ID', 'IMEI']

    # Define DB
    with Database.DB_Session_Scope() as DB_Module:

        # Add Record to DataBase
        for index, row in Data_File.iterrows():

            # Check for Existing
            Query = DB_Module.query(Models.Device).filter(Models.Device.Device_ID.like(str(row['Device_ID']))).first()

            # Record Not Found
            if not Query:

                # Create New Record
                New_Record = Models.Device(
                    Device_ID=str(row['Device_ID']),
                    Status_ID=int(row['Status_ID']),
                    Version_ID=int(row['Version_ID']),
                    Model_ID=int(row['Model_ID']),
                    IMEI=str(row['IMEI']),
                )

                # Add Record to DataBase
                try:
                
                    print(New_Record)

                    # Add Record to DataBase
                    DB_Module.add(New_Record)

                    # Increase New Count
                    New_Data_Count += 1

                except Exception as e:

                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding Device: {e}")

    # End Function
    return New_Data_Count

# Import Data_Type Data
def Import_Data_Type():

    # New Data Count Definition
    New_Data_Count = 0

    # Define Data File
    Data_File_Name = APP_Settings.DATA_REPOSITORY + APP_Settings.FILE_MEASUREMENT_TYPE

    # Download Data File
    try:
        
        # Download Data File
        Data_File = pd.read_csv(Data_File_Name)

    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"Data file read error.")

        # Exit
        exit()

    # Rename Columns
    Data_File.columns = ['Type_ID', 'Description', 'Variable', 'Unit', 'Segment']

    # Define DB
    with Database.DB_Session_Scope() as DB_Module:

        # Add Record to DataBase
        for index, row in Data_File.iterrows():

            # Check for Existing
            Query = DB_Module.query(Models.Data_Type).filter(Models.Data_Type.Type_ID.like(str(row['Type_ID']))).first()

            # Record Not Found
            if not Query:

                # Create New Record
                New_Record = Models.Data_Type(
                    Type_ID=int(row['Type_ID']),
                    Description=str(row['Description']),
                    Variable=str(row['Variable']),
                    Unit=str(row['Unit']),
                    Segment_ID=int(row['Segment']),                    
                )

                # Add Record to DataBase
                try:
                
                    # Add Record to DataBase
                    DB_Module.add(New_Record)

                    # Increase New Count
                    New_Data_Count += 1

                except Exception as e:

                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding Data_Type: {e}")

    # End Function
    return New_Data_Count

# Import SIM Data
def Import_SIM():

    # New Data Count Definition
    New_Data_Count = 0

    # Define Data File
    Data_File_Name = APP_Settings.DATA_REPOSITORY + APP_Settings.FILE_SIM

    # Download Data File
    try:
        
        # Download Data File
        Data_File = pd.read_csv(Data_File_Name)

    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"Data file read error.")

        # Exit
        exit()

    # Rename Columns
    Data_File.columns = ['SIM_ICCID', 'MCC_ID', 'MNC_ID', 'SIM_Number', 'SIM_Static_IP']

    # Define DB
    with Database.DB_Session_Scope() as DB_Module:

        # Add Record to DataBase
        for index, row in Data_File.iterrows():

            # Check for Existing
            Query = DB_Module.query(Models.SIM).filter(Models.SIM.ICCID.like(str(row['SIM_ICCID']))).first()

            # Record Not Found
            if not Query:

                # Create New Record
                New_Record = Models.SIM(
                    ICCID=str(row['SIM_ICCID']),
                    Operator_ID=int(row['MCC_ID']),
                    GSM_Number=str(row['SIM_Number']),
                    Static_IP=str(row['SIM_Static_IP']),
                )

                # Add Record to DataBase
                try:
                
                    # Add Record to DataBase
                    DB_Module.add(New_Record)

                    # Increase New Count
                    New_Data_Count += 1

                except Exception as e:

                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding SIM: {e}")

    # End Function
    return New_Data_Count

# Import Calibration Data
def Import_Calibration():

    # New Calibration Count Definition
    New_Data_Count = 0

    # Define Data File
    Data_File_Name = APP_Settings.DATA_REPOSITORY + APP_Settings.FILE_CALIBRATION

    # Download Data File
    try:
        
        # Download Data File
        Data_File = pd.read_csv(Data_File_Name)

    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"Data file read error.")

        # Exit
        exit()

    # Rename Columns
    Data_File.columns = ['Calibration_ID', 'Device_ID', 'Type_ID', 'Gain', 'Offset']

    # Define DB
    with Database.DB_Session_Scope() as DB_Module:

        # Add Record to DataBase
        for index, row in Data_File.iterrows():

            # Check for Existing
            Query = DB_Module.query(Models.Calibration).filter(Models.Calibration.Calibration_ID==int(row['Calibration_ID'])).first()

            # Record Not Found
            if not Query:

                # Create New Record
                New_Record = Models.Calibration(
                    Calibration_ID=int(row['Calibration_ID']),
                    Device_ID=str(row['Device_ID']),
                    Type_ID=int(row['Type_ID']),
                    Gain=float(row['Gain']),
                    Offset=float(row['Offset']),
                )

                # Add Record to DataBase
                try:
                
                    # Add Record to DataBase
                    DB_Module.add(New_Record)

                    # Increase New Count
                    New_Data_Count += 1

                except Exception as e:

                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding Calibration: {e}")

    # End Function
    return New_Data_Count

# Import Project Data
def Import_Project():

    # New Data Count Definition
    New_Data_Count = 0

    # Define Data File
    Data_File_Name = APP_Settings.DATA_REPOSITORY + APP_Settings.FILE_PROJECT

    # Download Data File
    try:
        
        # Download Data File
        Data_File = pd.read_csv(Data_File_Name)

    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"Data file read error.")

        # Exit
        exit()

    # Rename Columns
    Data_File.columns = ['Project_ID', 'Project_Name']

    # Define DB
    with Database.DB_Session_Scope() as DB_Module:

        # Add Record to DataBase
        for index, row in Data_File.iterrows():

            # Check for Existing
            Query = DB_Module.query(Models.Project).filter(Models.Project.Project_Name.like(str(row['Project_Name']))).first()

            # Record Not Found
            if not Query:

                # Create New Record
                New_Record = Models.Project(
                    Project_ID=int(row['Project_ID']),
                    Project_Name=str(row['Project_Name']),
                    Project_Description=str("-")
                )

                # Add Record to DataBase
                try:
                
                    # Add Record to DataBase
                    DB_Module.add(New_Record)

                    # Increase New Count
                    New_Data_Count += 1

                except Exception as e:

                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding Device: {e}")

    # End Function
    return New_Data_Count

# Data Segment
New_Data_Segment = Import_Data_Segment()
if New_Data_Segment > 0:
    Log.Terminal_Log("INFO", f"[{New_Data_Segment}] New Data Segment Added.")
else:
    Log.Terminal_Log("INFO", f"Data Segment is up to date.")

# GSM Operator
New_GSM_Operator = Import_GSM_Operator()
if New_GSM_Operator > 0:
    Log.Terminal_Log("INFO", f"[{New_GSM_Operator}] New GSM Operator Added.")
else:
    Log.Terminal_Log("INFO", f"GSM Operator is up to date.")

# Status
New_Status = Import_Status()
if New_Status > 0:
    Log.Terminal_Log("INFO", f"[{New_Status}] New Status Added.")
else:
    Log.Terminal_Log("INFO", f"Status is up to date.")

# Version
New_Version = Import_Version()
if New_Version > 0:
    Log.Terminal_Log("INFO", f"[{New_Version}] New Version Added.")
else:
    Log.Terminal_Log("INFO", f"Version is up to date.")

# Model
New_Model = Import_Model()
if New_Model > 0:
    Log.Terminal_Log("INFO", f"[{New_Model}] New Model Added.")
else:
    Log.Terminal_Log("INFO", f"Model is up to date.")

# Manufacturer
New_Manufacturer = Import_Manufacturer()
if New_Manufacturer > 0:
    Log.Terminal_Log("INFO", f"[{New_Manufacturer}] New Manufacturer Added.")
else:
    Log.Terminal_Log("INFO", f"Mamufacturer is up to date.")

# Modem
New_Modem = Import_Modem()
if New_Modem > 0:
    Log.Terminal_Log("INFO", f"[{New_Modem}] New Modem Added.")
else:
    Log.Terminal_Log("INFO", f"Modem is up to date.")

# Device
New_Device = Import_Device()
if New_Device > 0:
    Log.Terminal_Log("INFO", f"[{New_Device}] New Device Added.")
else:
    Log.Terminal_Log("INFO", f"Device is up to date.")

# Data_Type
New_Data_Type = Import_Data_Type()
if New_Data_Type > 0:
    Log.Terminal_Log("INFO", f"[{New_Data_Type}] New Data_Type Added.")
else:
    Log.Terminal_Log("INFO", f"Data_Type is up to date.")

# SIM
New_SIM = Import_SIM()
if New_SIM > 0:
    Log.Terminal_Log("INFO", f"[{New_SIM}] New SIM Added.")
else:
    Log.Terminal_Log("INFO", f"SIM is up to date.")

# Calibration
New_Calibration = Import_Calibration()
if New_Calibration > 0:
    Log.Terminal_Log("INFO", f"[{New_Calibration}] New Calibration Added.")
else:
    Log.Terminal_Log("INFO", f"Calibration is up to date.")

# Project
New_Project = Import_Project()
if New_Project > 0:
    Log.Terminal_Log("INFO", f"[{New_Project}] New Project Added.")
else:
    Log.Terminal_Log("INFO", f"Project is up to date.")