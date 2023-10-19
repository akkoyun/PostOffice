# Library Includes
from Setup import Database, Models, Log

# Define DB
DB_Module = Database.SessionLocal()

# MNC Table Add Record
def MNC_Initial_Values():
    
    try:

        # Create New DataStream
        GSM_MNC_Update = Models.GSM_MNC(
            Models.GSM_MNC(MNC_ID=1, MNC_Brand_Name="Turkcell", MNC_Operator_Name="Turkcell"),
            Models.GSM_MNC(MNC_ID=2, MNC_Brand_Name="Vodafone", MNC_Operator_Name="Vodafone"),
            Models.GSM_MNC(MNC_ID=3, MNC_Brand_Name="Türk Telekom", MNC_Operator_Name="Türk Telekom")
        )

        # Add Record to DataBase
        DB_Module.add(GSM_MNC_Update)

        # Commit DataBase
        DB_Module.commit()

        # Log Message
        Log.LOG_Message(f"GSM_MNC Table Default Values Updated")

    except Exception as e:

        # Log Message
        Log.LOG_Error_Message(f"An error occurred while adding GSM_MNC Table : {e}")

# MCC Table Add Record
def MCC_Initial_Values():
    
    try:

        # Create New DataStream
        GSM_MCC_Update = Models.GSM_MCC(
            Models.GSM_MCC(MCC_ID=286, MCC_ISO="TR", MCC_Country_Name="Turkey", MCC_Country_Code=90),
        )

        # Add Record to DataBase
        DB_Module.add(GSM_MCC_Update)

        # Commit DataBase
        DB_Module.commit()

        # Log Message
        Log.LOG_Message(f"GSM_MCC Table Default Values Updated")

    except Exception as e:

        # Log Message
        Log.LOG_Error_Message(f"An error occurred while adding GSM_MCC Table : {e}")

# Call Functions
MNC_Initial_Values()
MCC_Initial_Values()