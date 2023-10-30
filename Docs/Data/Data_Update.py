# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models, Log
import pandas as pd

# Import Operator Data
def Import_GSM_Operator():

    # Log Message
    Log.Terminal_Log("INFO", f"Control for New GSM Operator..")

    # New Operator Count
    New_Operator_Count = 0

    # Define DB
    DB_Module = Database.SessionLocal()

    try:

        # Read Operator File
        Operator_Data_File = pd.read_csv("Docs/Data/GSM_Operator.csv", skiprows=1, header=None)
        
        # Rename Columns
        Operator_Data_File.columns = ['MCC_ID', 'MCC_ISO', 'MCC_Country_Name', 'MCC_Country_Code', 'MCC_Country_Flag_Image_URL', 'MNC_ID', 'MNC_Brand_Name', 'MNC_Operator_Name', 'MNC_Operator_Image_URL']

        # Add Record to DataBase
        for index, row in Operator_Data_File.iterrows():

            # Check for Existing MCC_ID and MNC_ID
            Query_Operator = DB_Module.query(Models.Operator).filter(Models.Operator.MCC_ID==int(row['MCC_ID'])).filter(Models.Operator.MNC_ID==int(row['MNC_ID'])).first()

            # Record Not Found
            if not Query_Operator:

                # Create New Operator Record
                New_Operator_Record = Models.Operator(
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

    # Close DataBase
    DB_Module.close()

    # Log Message
    if New_Operator_Count > 0:
        Log.Terminal_Log("INFO", f"[{New_Operator_Count}] New GSM Operator Recorded.")
    else:
        Log.Terminal_Log("INFO", f"GSM Operator is up to date")

# Import SIM
def Import_SIM():

    # Log Message
    Log.Terminal_Log("INFO", f"Control for New SIM Record..")

    # New SIM Count
    New_SIM_Count = 0

    # Define DB
    DB_Module = Database.SessionLocal()

    try:

        # Read SIM File
        SIM_Data_File = pd.read_csv("Docs/Data/SIM_Record.csv", sep=",")
        
        # Add Record to DataBase
        for index, row in SIM_Data_File.iterrows():
            
            # Check for Existing ICCID
            Query_SIM = DB_Module.query(Models.SIM).filter(Models.SIM.ICCID.like(str(row['SIM_ICCID']))).first()
            
            # Record Not Found
            if not Query_SIM:

                # Check for Existing Operator
                Query_SIM = DB_Module.query(Models.Operator).filter(Models.Operator.MCC_ID==int(row['MCC_ID'])).filter(Models.Operator.MNC_ID==int(row['MNC_ID'])).first()

                # Control for Record
                if Query_SIM:

                    # Get Operator ID
                    Operator_ID = Query_SIM.Operator_ID

                # Operator Not Found
                else:

                    # Set Operator ID
                    Operator_ID = 0

                # Create New SIM Record
                New_SIM_Record = Models.SIM(
                    ICCID = row['SIM_ICCID'],
                    Operator_ID = Operator_ID,
                    GSM_Number = row['SIM_Number'],
                    Static_IP = row['SIM_Static_IP'],
                )
                
                # Add Record to DataBase
                try:

                    # Add Record to DataBase
                    DB_Module.add(New_SIM_Record)

                    # Flush DataBase
                    DB_Module.flush()

                    # Commit DataBase
                    DB_Module.commit()

                    # Increase New SIM Count
                    New_SIM_Count += 1

                except Exception as e:
                    
                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding SIM: {e}")
                    
                    # Rollback DataBase
                    DB_Module.rollback()

    # Catch Errors
    except Exception as e:
        
        # Log Message
        Log.Terminal_Log("ERROR", f"An error occurred while adding SIM: {e}")

    # Close DataBase
    DB_Module.close()

    # Log Message
    if New_SIM_Count > 0:
        Log.Terminal_Log("INFO", f"[{New_SIM_Count}] New SIM Recorded.")
    else:
        Log.Terminal_Log("INFO", f"SIM table is up to date")

# Import Manufacturer Data
def Import_Manufacturer():

    # Log Message
    Log.Terminal_Log("INFO", f"Control for New Manufacturer..")

    # New Manufacturer Count
    New_Manufacturer_Count = 0

    # Define DB
    DB_Module = Database.SessionLocal()

    try:

        # Read Manufacturer File
        Manufacturer_Data_File = pd.read_csv("Docs/Data/Manufacturer.csv", skiprows=1, header=None)
        
        # Rename Columns
        Manufacturer_Data_File.columns = ['Manufacturer_ID', 'Manufacturer']

        # Add Record to DataBase
        for index, row in Manufacturer_Data_File.iterrows():

            # Check for Existing Manufacturer_ID
            Query_Manufacturer = DB_Module.query(Models.Manufacturer).filter(Models.Manufacturer.Manufacturer_ID==int(row['Manufacturer_ID'])).first()

            # Record Not Found
            if not Query_Manufacturer:

                # Create New Manufacturer Record
                New_Manufacturer_Record = Models.Manufacturer(
                    Manufacturer_ID=int(row['Manufacturer_ID']),
                    Manufacturer=str(row['Manufacturer']),
                )

                # Add Record to DataBase
                try:
                
                    # Add Record to DataBase
                    DB_Module.add(New_Manufacturer_Record)

                    # Flush DataBase
                    DB_Module.flush()
                    
                    # Commit DataBase
                    DB_Module.commit()

                    # Increase New Manufacturer Count
                    New_Manufacturer_Count += 1
                    
                except Exception as e:
                    
                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding Manufacturer: {e}")
                    
                    # Rollback DataBase
                    DB_Module.rollback()

    # Catch Errors
    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"An error occurred while adding Manufacturer: {e}")

    # Close DataBase
    DB_Module.close()

    # Log Message
    if New_Manufacturer_Count > 0:
        Log.Terminal_Log("INFO", f"[{New_Manufacturer_Count}] New Manufacturer Recorded.")
    else:
        Log.Terminal_Log("INFO", f"Manufacturer is up to date")

# Import Model Data
def Import_Model():

    # Log Message
    Log.Terminal_Log("INFO", f"Control for New Model..")

    # New Model Count
    New_Model_Count = 0

    # Define DB
    DB_Module = Database.SessionLocal()

    try:

        # Read Model File
        Model_Data_File = pd.read_csv("Docs/Data/Model.csv", skiprows=1, header=None)
        
        # Rename Columns
        Model_Data_File.columns = ['Model_ID', 'Model']

        # Add Record to DataBase
        for index, row in Model_Data_File.iterrows():

            # Check for Existing Model_ID
            Query_Model = DB_Module.query(Models.Model).filter(Models.Model.Model_ID==int(row['Model_ID'])).first()

            # Record Not Found
            if not Query_Model:

                # Create New Model Record
                New_Model_Record = Models.Model(
                    Model_ID=int(row['Model_ID']),
                    Model=str(row['Model']),
                )

                # Add Record to DataBase
                try:
                
                    # Add Record to DataBase
                    DB_Module.add(New_Model_Record)

                    # Flush DataBase
                    DB_Module.flush()
                    
                    # Commit DataBase
                    DB_Module.commit()

                    # Increase New Model Count
                    New_Model_Count += 1
                    
                except Exception as e:
                    
                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding Model: {e}")
                    
                    # Rollback DataBase
                    DB_Module.rollback()

    # Catch Errors
    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"An error occurred while adding Model: {e}")

    # Close DataBase
    DB_Module.close()

    # Log Message
    if New_Model_Count > 0:
        Log.Terminal_Log("INFO", f"[{New_Model_Count}] New Manufacturer Recorded.")
    else:
        Log.Terminal_Log("INFO", f"Manufacturer is up to date")

# Import Measurement_Type Data
def Import_Measurement_Type():

    # Log Message
    Log.Terminal_Log("INFO", f"Control for New Measurement_Type..")

    # New Measurement_Type Count
    New_Measurement_Type_Count = 0

    # Define DB
    DB_Module = Database.SessionLocal()

    try:

        # Read Measurement_Type File
        Measurement_Type_Data_File = pd.read_csv("Docs/Data/Measurement_Type.csv", skiprows=1, header=None)
        
        # Rename Columns
        Measurement_Type_Data_File.columns = ['Type_ID', 'Description', 'Variable', 'Unit', 'Segment']

        # Add Record to DataBase
        for index, row in Measurement_Type_Data_File.iterrows():

            # Check for Existing Measurement_Type_ID
            Query_Measurement_Type = DB_Module.query(Models.Measurement_Type).filter(Models.Measurement_Type.Type_ID==int(row['Type_ID'])).first()

            # Record Not Found
            if not Query_Measurement_Type:

                # Create New Measurement_Type Record
                New_Measurement_Type_Record = Models.Measurement_Type(
                    Type_ID=int(row['Type_ID']),
                    Description=str(row['Description']),
                    Variable=str(row['Variable']),
                    Unit=str(row['Unit']),
                    Segment=int(row['Segment']),
                )

                # Add Record to DataBase
                try:
                
                    # Add Record to DataBase
                    DB_Module.add(New_Measurement_Type_Record)

                    # Flush DataBase
                    DB_Module.flush()
                    
                    # Commit DataBase
                    DB_Module.commit()

                    # Increase New Measurement_Type Count
                    New_Measurement_Type_Count += 1
                    
                except Exception as e:
                    
                    # Log Message
                    Log.Terminal_Log("ERROR", f"An error occurred while adding Measurement Type: {e}")
                    
                    # Rollback DataBase
                    DB_Module.rollback()

    # Catch Errors
    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"An error occurred while adding Measurement Type: {e}")

    # Close DataBase
    DB_Module.close()

    # Log Message
    if New_Measurement_Type_Count > 0:
        Log.Terminal_Log("INFO", f"[{New_Measurement_Type_Count}] New Measurement Type Recorded.")
    else:
        Log.Terminal_Log("INFO", f"Measurement Type is up to date")


# Test Function
Import_GSM_Operator()
Import_SIM()
Import_Manufacturer()
Import_Model()
Import_Measurement_Type()