# Library Includes
from Setup import Database, Models, Log

# Define DB
DB_Module = Database.SessionLocal()

# MNC Table Add Record
def MNC_Initial_Values():
    
    try:

        # Define MNC Records
        MNC_Records = [
            Models.GSM_MNC(MCC_ID=286, MNC_ID=1, MNC_Brand_Name="Turkcell", MNC_Operator_Name="Turkcell"),
            Models.GSM_MNC(MCC_ID=286, MNC_ID=2, MNC_Brand_Name="Vodafone", MNC_Operator_Name="Vodafone"),
            Models.GSM_MNC(MCC_ID=286, MNC_ID=3, MNC_Brand_Name="Türk Telekom", MNC_Operator_Name="Türk Telekom")
        ]

        # Add Record to DataBase
        for record in MNC_Records:

            # Check for Existing Record
            Query_Record = DB_Module.query(Models.GSM_MNC).filter(Models.GSM_MNC.MNC_ID.like(record.MNC_ID)).first()

            # Record Not Found
            if not Query_Record:

                # Add Record to DataBase
                DB_Module.add(record)

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

        # Define MCC Records
        MCC_Records = [
            Models.GSM_MCC(MCC_ID=286, MCC_ISO="TR", MCC_Country_Name="Turkey", MCC_Country_Code=90),
        ]

        # Add Record to DataBase
        for record in MCC_Records:
            DB_Module.add(record)

        # Commit DataBase
        DB_Module.commit()

        # Log Message
        Log.LOG_Message(f"GSM_MCC Table Default Values Updated")

    except Exception as e:

        # Log Message
        Log.LOG_Error_Message(f"An error occurred while adding GSM_MCC Table : {e}")

# GSM Module Type Add Record
def Module_Type_Initial_Values():
    
    try:

        # Define MCC Records
        Module_Type_Records = [
            Models.Module_Type(Module_Type_ID=0, Module_Type_Name="Unknown"),
            Models.Module_Type(Module_Type_ID=1, Module_Type_Name="GSM"),
            Models.Module_Type(Module_Type_ID=2, Module_Type_Name="LORA"),
            Models.Module_Type(Module_Type_ID=3, Module_Type_Name="NB-IOT"),
        ]

        # Add Record to DataBase
        for record in Module_Type_Records:
            DB_Module.add(record)

        # Commit DataBase
        DB_Module.commit()

        # Log Message
        Log.LOG_Message(f"Module_Type Table Default Values Updated")

    except Exception as e:

        # Log Message
        Log.LOG_Error_Message(f"An error occurred while adding Module_Type Table : {e}")

# GSM Module Manufacturer Add Record
def GSM_Manufacturer_Initial_Values():
    
    try:

        # Define MNC Records
        Manufacturer_Records = [
            Models.Module_Manufacturer(Module_Manufacturer_ID=0, Module_Manufacturer_Name="Unknown"),
            Models.Module_Manufacturer(Module_Manufacturer_ID=1, Module_Manufacturer_Name="Telit"),
        ]

        # Add Record to DataBase
        for record in Manufacturer_Records:
            DB_Module.add(record)
        
        # Commit DataBase
        DB_Module.commit()

        # Log Message
        Log.LOG_Message(f"Module_Manufacturer Table Default Values Updated")

    except Exception as e:

        # Log Message
        Log.LOG_Error_Message(f"An error occurred while adding Module_Manufacturer Table : {e}")

# GSM Module Model Add Record
def GSM_Model_Initial_Values():
    
    try:

        # Define MNC Records
        Model_Records = [
            Models.Module_Model(Module_Model_ID=0, Module_Model_Name="Unknown"),
            Models.Module_Model(Module_Model_ID=1, Module_Model_Name="GE910 QUAD"),
            Models.Module_Model(Module_Model_ID=2, Module_Model_Name="GE910 QUAD V3"),
            Models.Module_Model(Module_Model_ID=3, Module_Model_Name="GE910 GNSS"),
            Models.Module_Model(Module_Model_ID=4, Module_Model_Name="LE910 S1 EA"),
            Models.Module_Model(Module_Model_ID=5, Module_Model_Name="LE910 S1 EAG"),
            Models.Module_Model(Module_Model_ID=6, Module_Model_Name="LE910 R1 EU"),
            Models.Module_Model(Module_Model_ID=7, Module_Model_Name="LE910 C1 EUX"),
        ]

        # Add Record to DataBase
        for record in Model_Records:
            DB_Module.add(record)
        
        # Commit DataBase
        DB_Module.commit()

        # Log Message
        Log.LOG_Message(f"Module_Model Table Default Values Updated")

    except Exception as e:

        # Log Message
        Log.LOG_Error_Message(f"An error occurred while adding Module_Model Table : {e}")

# Call Functions
MNC_Initial_Values()
MCC_Initial_Values()
Module_Type_Initial_Values()
GSM_Manufacturer_Initial_Values()
GSM_Model_Initial_Values()