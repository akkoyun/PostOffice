# Setup Root Path
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup.Config import APP_Settings
from Setup import Models, Database
import sys
from Functions import Log
import pandas as pd

# Import Data_Segment Data
def Import_Data_Segment(DB_Module):

    # Log Message
    Log.Terminal_Log("DEBUG", f"Updating New Data_Segment Table..")

    # New Count
    New_Count = 0

    try:

        # Read File
        Data_File = pd.read_csv(f"{APP_Settings.FILE_DATA_SEGMENT}", skiprows=1, header=None)
        
        # Rename Columns
        Data_File.columns = ['Segment_ID', 'Description']

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

                    # Flush DataBase
                    DB_Module.flush()
                    
                    # Commit DataBase
                    DB_Module.commit()

                    # Increase New Count
                    New_Count += 1
                    
                except Exception as e:
                    
                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding Data_Segment: {e}")
                    
                    # Rollback DataBase
                    DB_Module.rollback()

    # Catch Errors
    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"An error occurred while adding Data_Segment: {e}")

    # Log Message
    if New_Count > 0:
        
        # Log Message
        Log.Terminal_Log("DEBUG", f"[{New_Count}] New Data Segment Recorded.")

    else:

        # Log Message
        Log.Terminal_Log("DEBUG", f"Data_Segment is up to date")

# Import Operator Data
def Import_GSM_Operator(DB_Module):

    # Log Message
    Log.Terminal_Log("DEBUG", f"Control for New GSM Operator..")

    # New Operator Count
    New_Operator_Count = 0

    try:

        # Read Operator File
        Operator_Data_File = pd.read_csv(f"{APP_Settings.FILE_GSM_OPERATOR}", skiprows=1, header=None)
        
        # Rename Columns
        Operator_Data_File.columns = ['MCC_ID', 'MCC_ISO', 'MCC_Country_Name', 'MCC_Country_Code', 'MCC_Country_Flag_Image_URL', 'MNC_ID', 'MNC_Brand_Name', 'MNC_Operator_Name', 'MNC_Operator_Image_URL']

        # Add Record to DataBase
        for index, row in Operator_Data_File.iterrows():

            # Check for Existing MCC_ID and MNC_ID
            Query_Operator = DB_Module.query(Models.GSM_Operator).filter(Models.GSM_Operator.MCC_ID==int(row['MCC_ID'])).filter(Models.GSM_Operator.MNC_ID==int(row['MNC_ID'])).first()

            # Record Not Found
            if not Query_Operator:

                # Create New Operator Record
                New_Operator_Record = Models.GSM_Operator(
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
                    DB_Module.add(New_Operator_Record)

                    # Flush DataBase
                    DB_Module.flush()
                    
                    # Commit DataBase
                    DB_Module.commit()

                    # Increase New Operator Count
                    New_Operator_Count += 1
                    
                except Exception as e:
                    
                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding SIM: {e}")
                    
                    # Rollback DataBase
                    DB_Module.rollback()

    # Catch Errors
    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"An error occurred while adding Operator: {e}")

    # Log Message
    if New_Operator_Count > 0:
        
        # Log Message
        Log.Terminal_Log("DEBUG", f"[{New_Operator_Count}] New GSM Operator Recorded.")

    else:

        # Log Message
        Log.Terminal_Log("DEBUG", f"GSM Operator is up to date")

# Import Status Data
def Import_Status(DB_Module):

    # Log Message
    Log.Terminal_Log("DEBUG", f"Updating New Status Table..")

    # New Count
    New_Count = 0

    try:

        # Read File
        Data_File = pd.read_csv(f"{APP_Settings.FILE_STATUS}", skiprows=1, header=None)
        
        # Rename Columns
        Data_File.columns = ['Status_ID', 'Description']

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

                    # Flush DataBase
                    DB_Module.flush()
                    
                    # Commit DataBase
                    DB_Module.commit()

                    # Increase New Count
                    New_Count += 1
                    
                except Exception as e:
                    
                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding Status: {e}")
                    
                    # Rollback DataBase
                    DB_Module.rollback()

    # Catch Errors
    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"An error occurred while adding Status: {e}")

    # Log Message
    if New_Count > 0:
        
        # Log Message
        Log.Terminal_Log("DEBUG", f"[{New_Count}] New Status Recorded.")

    else:

        # Log Message
        Log.Terminal_Log("DEBUG", f"Status is up to date")

# Import Version Data
def Import_Version(DB_Module):

    # Log Message
    Log.Terminal_Log("DEBUG", f"Updating New Version Table..")

    # New Count
    New_Count = 0

    try:

        # Read File
        Data_File = pd.read_csv(f"{APP_Settings.FILE_VERSION}", skiprows=1, header=None)
        
        # Rename Columns
        Data_File.columns = ['Version_ID', 'Firmware']

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

                    # Flush DataBase
                    DB_Module.flush()
                    
                    # Commit DataBase
                    DB_Module.commit()

                    # Increase New Count
                    New_Count += 1
                    
                except Exception as e:
                    
                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding Version: {e}")
                    
                    # Rollback DataBase
                    DB_Module.rollback()

    # Catch Errors
    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"An error occurred while adding Version: {e}")

    # Log Message
    if New_Count > 0:
        
        # Log Message
        Log.Terminal_Log("DEBUG", f"[{New_Count}] New Version Recorded.")

    else:

        # Log Message
        Log.Terminal_Log("DEBUG", f"Version is up to date")

# Import Model Data
def Import_Model(DB_Module):

    # Log Message
    Log.Terminal_Log("DEBUG", f"Updating New Model Table..")

    # New Count
    New_Count = 0

    try:

        # Read File
        Data_File = pd.read_csv(f"{APP_Settings.FILE_MODEL}", skiprows=1, header=None)
        
        # Rename Columns
        Data_File.columns = ['Model_ID', 'Model']

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

                    # Flush DataBase
                    DB_Module.flush()
                    
                    # Commit DataBase
                    DB_Module.commit()

                    # Increase New Count
                    New_Count += 1
                    
                except Exception as e:
                    
                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding Model: {e}")
                    
                    # Rollback DataBase
                    DB_Module.rollback()

    # Catch Errors
    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"An error occurred while adding Model: {e}")

    # Log Message
    if New_Count > 0:
        
        # Log Message
        Log.Terminal_Log("DEBUG", f"[{New_Count}] New Model Recorded.")

    else:

        # Log Message
        Log.Terminal_Log("DEBUG", f"Model is up to date")

# Import Manufacturer Data
def Import_Manufacturer(DB_Module):

    # Log Message
    Log.Terminal_Log("DEBUG", f"Updating New Manufacturer Table..")

    # New Count
    New_Count = 0

    try:

        # Read File
        Data_File = pd.read_csv(f"{APP_Settings.FILE_MANUFACTURER}", skiprows=1, header=None)
        
        # Rename Columns
        Data_File.columns = ['Manufacturer_ID', 'Manufacturer']

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

                    # Flush DataBase
                    DB_Module.flush()
                    
                    # Commit DataBase
                    DB_Module.commit()

                    # Increase New Count
                    New_Count += 1
                    
                except Exception as e:
                    
                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding Manufacturer: {e}")
                    
                    # Rollback DataBase
                    DB_Module.rollback()

    # Catch Errors
    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"An error occurred while adding Manufacturer: {e}")

    # Log Message
    if New_Count > 0:
        
        # Log Message
        Log.Terminal_Log("DEBUG", f"[{New_Count}] New Manufacturer Recorded.")

    else:

        # Log Message
        Log.Terminal_Log("DEBUG", f"Manufacturer is up to date")

# Import Modem Data
def Import_Modem(DB_Module):

    # Log Message
    Log.Terminal_Log("DEBUG", f"Updating New Modem Table..")

    # New Count
    New_Count = 0

    try:

        # Read File
        Data_File = pd.read_csv(f"{APP_Settings.FILE_MODEM}", skiprows=1, header=None)
        
        # Rename Columns
        Data_File.columns = ['IMEI', 'Model_ID', 'Manufacturer_ID']

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

                    # Flush DataBase
                    DB_Module.flush()
                    
                    # Commit DataBase
                    DB_Module.commit()

                    # Increase New Count
                    New_Count += 1
                    
                except Exception as e:
                    
                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding Modem: {e}")
                    
                    # Rollback DataBase
                    DB_Module.rollback()

    # Catch Errors
    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"An error occurred while adding Modem: {e}")

    # Log Message
    if New_Count > 0:
        
        # Log Message
        Log.Terminal_Log("DEBUG", f"[{New_Count}] New Modem Recorded.")

    else:

        # Log Message
        Log.Terminal_Log("DEBUG", f"Modem is up to date")

# Import Device Data
def Import_Device(DB_Module):

    # Log Message
    Log.Terminal_Log("DEBUG", f"Updating New Device Table..")

    # New Count
    New_Count = 0

    try:

        # Read File
        Data_File = pd.read_csv(f"{APP_Settings.FILE_DEVICE}", skiprows=1, header=None)
        
        # Rename Columns
        Data_File.columns = ['Device_ID', 'Status_ID', 'Version_ID', 'Model_ID', 'IMEI']

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
                
                    # Add Record to DataBase
                    DB_Module.add(New_Record)

                    # Flush DataBase
                    DB_Module.flush()
                    
                    # Commit DataBase
                    DB_Module.commit()

                    # Increase New Count
                    New_Count += 1
                    
                except Exception as e:
                    
                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding Device: {e}")
                    
                    # Rollback DataBase
                    DB_Module.rollback()

    # Catch Errors
    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"An error occurred while adding Device: {e}")

    # Log Message
    if New_Count > 0:
        
        # Log Message
        Log.Terminal_Log("DEBUG", f"[{New_Count}] New Device Recorded.")

    else:

        # Log Message
        Log.Terminal_Log("DEBUG", f"Device is up to date")

# Import Data_Type Data
def Import_Data_Type(DB_Module):

    # Log Message
    Log.Terminal_Log("DEBUG", f"Updating New Data_Type Table..")

    # New Count
    New_Count = 0

    try:

        # Read File
        Data_File = pd.read_csv(f"{APP_Settings.FILE_MEASUREMENT_TYPE}", skiprows=1, header=None)
        
        # Rename Columns
        Data_File.columns = ['Type_ID', 'Description', 'Variable', 'Unit', 'Segment']

        # Add Record to DataBase
        for index, row in Data_File.iterrows():

            # Check for Existing
            Query = DB_Module.query(Models.Data_Type).filter(Models.Data_Type.Variable.like(str(row['Variable']))).first()

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

                    # Flush DataBase
                    DB_Module.flush()
                    
                    # Commit DataBase
                    DB_Module.commit()

                    # Increase New Count
                    New_Count += 1
                    
                except Exception as e:
                    
                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding Data_Type: {e}")
                    
                    # Rollback DataBase
                    DB_Module.rollback()

    # Catch Errors
    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"An error occurred while adding Data_Type: {e}")

    # Log Message
    if New_Count > 0:
        
        # Log Message
        Log.Terminal_Log("DEBUG", f"[{New_Count}] New Data_Type Recorded.")

    else:

        # Log Message
        Log.Terminal_Log("DEBUG", f"Data_Type is up to date")

# Import SIM Data
def Import_SIM(DB_Module):

    # Log Message
    Log.Terminal_Log("DEBUG", f"Updating New SIM Table..")

    # New Count
    New_Count = 0

    try:

        # Read File
        Data_File = pd.read_csv(f"{APP_Settings.FILE_SIM}", skiprows=1, header=None)
        
        # Rename Columns
        Data_File.columns = ['SIM_ICCID', 'MCC_ID', 'MNC_ID', 'SIM_Number', 'SIM_Static_IP']

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

                    # Flush DataBase
                    DB_Module.flush()
                    
                    # Commit DataBase
                    DB_Module.commit()

                    # Increase New Count
                    New_Count += 1
                    
                except Exception as e:
                    
                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding SIM: {e}")
                    
                    # Rollback DataBase
                    DB_Module.rollback()

    # Catch Errors
    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"An error occurred while adding SIM: {e}")

    # Log Message
    if New_Count > 0:
        
        # Log Message
        Log.Terminal_Log("DEBUG", f"[{New_Count}] New SIM Recorded.")

    else:

        # Log Message
        Log.Terminal_Log("DEBUG", f"SIM is up to date")

# Define DB
DB_Module = Database.SessionLocal()

# Create DB Models
Models.Base.metadata.create_all(bind=Database.DB_Engine, checkfirst=True)

# Update DataBase
Import_Data_Segment(DB_Module)
Import_GSM_Operator(DB_Module)
Import_Status(DB_Module)
Import_Version(DB_Module)
Import_Model(DB_Module)
Import_Manufacturer(DB_Module)
Import_Modem(DB_Module)
Import_Device(DB_Module)
Import_Data_Type(DB_Module)
Import_SIM(DB_Module)

# Close Database
DB_Module.close()