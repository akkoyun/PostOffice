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
            Query_Operator = DB_Module.query(Models.Operator).filter(Models.Operator.MCC_ID == int(row['MCC_ID'])).filter(Models.Operator.MNC_ID == int(row['MNC_ID'])).first()

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
    finally:

        # Close DataBase
        DB_Module.close()

    # Log Message
    if New_Operator_Count > 0:
        Log.Terminal_Log("INFO", f"[{New_Operator_Count}] New GSM Operator Recorded.")
    else:
        Log.Terminal_Log("INFO", f"GSM Operator is up to date")

# Import SIM
def Import_SIM():

    # Define DB
    DB_Module = Database.SessionLocal()

    try:

        # Read SIM File
        SIM_Data_File = pd.read_csv("Docs/Data/SIM_Record.cvs", sep=",")
        
        # Add Record to DataBase
        for row in SIM_Data_File.iterrows():
            
            # Check for Existing ICCID
            Query_SIM = DB_Module.query(Models.SIM).filter(Models.SIM.SIM_ICCID.like(str(row['SIM_ICCID']))).first()
            
            # Record Not Found
            if not Query_SIM:

                # Create New Module Record
                New_SIM_Record = Models.SIM(
                    ICCID=row['SIM_ICCID'],
                    Operator_ID=0,
                    GSM_Number=row['SIM_Number'],
                    Static_IP=row['SIM_Static_IP'],
                )
                
                # Add Record to DataBase
                try:

                    # Add Record to DataBase
                    DB_Module.add(New_SIM_Record)

                    # Flush DataBase
                    DB_Module.flush()

                    # Commit DataBase
                    DB_Module.commit()
                    
                    # Log Message
                    Log.Terminal_Log("INFO", "New SIM Recorded.")
                    
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
    finally:

        # Close DataBase
        DB_Module.close()

