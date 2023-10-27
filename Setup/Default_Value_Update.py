# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models, Log
import pandas as pd

# Define DB
DB_Module = Database.SessionLocal()

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

            # Check for Existing Record
            Query_Record = DB_Module.query(Models.Module_Type).filter(Models.Module_Type.Module_Type_ID==(record.Module_Type_ID)).first()

            # Record Not Found
            if not Query_Record:

                # Add Record to DataBase
                DB_Module.add(record)

        # Commit DataBase
        DB_Module.commit()

        # Log Message
        Log.Terminal_Log("INFO", f"Module_Type Table Default Values Updated")

    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"An error occurred while adding Module_Type Table : {e}")

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

            # Check for Existing Record
            Query_Record = DB_Module.query(Models.Module_Manufacturer).filter(Models.Module_Manufacturer.Module_Manufacturer_ID==(record.Module_Manufacturer_ID)).first()

            # Record Not Found
            if not Query_Record:

                # Add Record to DataBase
                DB_Module.add(record)
        
        # Commit DataBase
        DB_Module.commit()

        # Log Message
        Log.Terminal_Log("INFO", f"Module_Manufacturer Table Default Values Updated")

    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"An error occurred while adding Module_Manufacturer Table : {e}")

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

            # Check for Existing Record
            Query_Record = DB_Module.query(Models.Module_Model).filter(Models.Module_Model.Module_Model_ID==(record.Module_Model_ID)).first()

            # Record Not Found
            if not Query_Record:

                # Add Record to DataBase
                DB_Module.add(record)
        
        # Commit DataBase
        DB_Module.commit()

        # Log Message
        Log.Terminal_Log("INFO", f"Module_Model Table Default Values Updated")

    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"An error occurred while adding Module_Model Table : {e}")

# Measurment Type Add Record
def Measurement_Type_Initial_Values():
    
    try:

        # Define Measurement Type Records
        Model_Records = [

            # Device        - 1
            # Power         - 2
            # Environment   - 3
            # Water         - 4
            # Energy        - 5
            # Battery       - 6

            # Unknown Measurement Type
            Models.Measurement_Type(Measurement_Type_ID=0, Measurement_Type_Name="Unknown", Measurement_Type_Variable="", Measurement_Type_Unit="", Measurement_Type_Segment="Unknown"),

            # Battery Measurement Types
            Models.Measurement_Type(Measurement_Type_ID=101, Measurement_Type_Name="Battery Instant Voltage", Measurement_Type_Variable="IV", Measurement_Type_Unit="V", Measurement_Type_Segment="Battery"),
            Models.Measurement_Type(Measurement_Type_ID=102, Measurement_Type_Name="Battery Average Current", Measurement_Type_Variable="AC", Measurement_Type_Unit="mA", Measurement_Type_Segment="Battery"),
            Models.Measurement_Type(Measurement_Type_ID=103, Measurement_Type_Name="Battery State of Charge", Measurement_Type_Variable="SOC", Measurement_Type_Unit="%", Measurement_Type_Segment="Battery"),
            Models.Measurement_Type(Measurement_Type_ID=104, Measurement_Type_Name="Battery Temperature", Measurement_Type_Variable="T", Measurement_Type_Unit="C", Measurement_Type_Segment="Battery"),
            Models.Measurement_Type(Measurement_Type_ID=105, Measurement_Type_Name="Battery Full Capacity", Measurement_Type_Variable="FB", Measurement_Type_Unit="mAh", Measurement_Type_Segment="Battery"),
            Models.Measurement_Type(Measurement_Type_ID=106, Measurement_Type_Name="Battery Instant Capacity", Measurement_Type_Variable="IB", Measurement_Type_Unit="mAh", Measurement_Type_Segment="Battery"),
            Models.Measurement_Type(Measurement_Type_ID=107, Measurement_Type_Name="Battery Charge State", Measurement_Type_Variable="Charge", Measurement_Type_Unit="-", Measurement_Type_Segment="Battery"),

            # Environment Measurement Types
            Models.Measurement_Type(Measurement_Type_ID=311, Measurement_Type_Name="Air Temperature", Measurement_Type_Variable="AT", Measurement_Type_Unit="C", Measurement_Type_Segment="Environment"),
            Models.Measurement_Type(Measurement_Type_ID=312, Measurement_Type_Name="Air Humidity", Measurement_Type_Variable="AH", Measurement_Type_Unit="%", Measurement_Type_Segment="Environment"),
            Models.Measurement_Type(Measurement_Type_ID=313, Measurement_Type_Name="Air Pressure", Measurement_Type_Variable="AP", Measurement_Type_Unit="hPa", Measurement_Type_Segment="Environment"),
            Models.Measurement_Type(Measurement_Type_ID=314, Measurement_Type_Name="UV Index", Measurement_Type_Variable="UV", Measurement_Type_Unit="-", Measurement_Type_Segment="Environment"),
            Models.Measurement_Type(Measurement_Type_ID=315, Measurement_Type_Name="Visual Light", Measurement_Type_Variable="VL", Measurement_Type_Unit="Lux", Measurement_Type_Segment="Environment"),
            Models.Measurement_Type(Measurement_Type_ID=316, Measurement_Type_Name="Infrared Light", Measurement_Type_Variable="IL", Measurement_Type_Unit="Lux", Measurement_Type_Segment="Environment"),
            
            # Soil Temperature Measurement Types
            Models.Measurement_Type(Measurement_Type_ID=320, Measurement_Type_Name="Soil Temperature 0", Measurement_Type_Variable="ST0", Measurement_Type_Unit="C", Measurement_Type_Segment="Environment"),
            Models.Measurement_Type(Measurement_Type_ID=321, Measurement_Type_Name="Soil Temperature 1", Measurement_Type_Variable="ST1", Measurement_Type_Unit="C", Measurement_Type_Segment="Environment"),
            Models.Measurement_Type(Measurement_Type_ID=322, Measurement_Type_Name="Soil Temperature 2", Measurement_Type_Variable="ST2", Measurement_Type_Unit="C", Measurement_Type_Segment="Environment"),
            Models.Measurement_Type(Measurement_Type_ID=323, Measurement_Type_Name="Soil Temperature 3", Measurement_Type_Variable="ST3", Measurement_Type_Unit="C", Measurement_Type_Segment="Environment"),
            Models.Measurement_Type(Measurement_Type_ID=324, Measurement_Type_Name="Soil Temperature 4", Measurement_Type_Variable="ST4", Measurement_Type_Unit="C", Measurement_Type_Segment="Environment"),
            Models.Measurement_Type(Measurement_Type_ID=325, Measurement_Type_Name="Soil Temperature 5", Measurement_Type_Variable="ST5", Measurement_Type_Unit="C", Measurement_Type_Segment="Environment"),
            Models.Measurement_Type(Measurement_Type_ID=326, Measurement_Type_Name="Soil Temperature 6", Measurement_Type_Variable="ST6", Measurement_Type_Unit="C", Measurement_Type_Segment="Environment"),
            Models.Measurement_Type(Measurement_Type_ID=327, Measurement_Type_Name="Soil Temperature 7", Measurement_Type_Variable="ST7", Measurement_Type_Unit="C", Measurement_Type_Segment="Environment"),
            Models.Measurement_Type(Measurement_Type_ID=328, Measurement_Type_Name="Soil Temperature 8", Measurement_Type_Variable="ST8", Measurement_Type_Unit="C", Measurement_Type_Segment="Environment"),
            Models.Measurement_Type(Measurement_Type_ID=329, Measurement_Type_Name="Soil Temperature 9", Measurement_Type_Variable="ST9", Measurement_Type_Unit="C", Measurement_Type_Segment="Environment"),
            
            # Rain Measurement Types
            Models.Measurement_Type(Measurement_Type_ID=331, Measurement_Type_Name="Rain", Measurement_Type_Variable="R", Measurement_Type_Unit="m/sn", Measurement_Type_Segment="Environment"),
            
            # Wind Measurement Types
            Models.Measurement_Type(Measurement_Type_ID=341, Measurement_Type_Name="Wind Speed", Measurement_Type_Variable="WS", Measurement_Type_Unit="m/sn", Measurement_Type_Segment="Environment"),
            Models.Measurement_Type(Measurement_Type_ID=342, Measurement_Type_Name="Wind Direction", Measurement_Type_Variable="WD", Measurement_Type_Unit="Degree", Measurement_Type_Segment="Environment"),
            
            # Water Pressure Measurement Types
            Models.Measurement_Type(Measurement_Type_ID=351, Measurement_Type_Name="Water Pressure IN", Measurement_Type_Variable="PIN", Measurement_Type_Unit="Bar", Measurement_Type_Segment="Environment"),
            Models.Measurement_Type(Measurement_Type_ID=352, Measurement_Type_Name="Water Pressure OUT", Measurement_Type_Variable="POUT", Measurement_Type_Unit="Bar", Measurement_Type_Segment="Environment"),
            
            # Water Flow Measurement Types
            Models.Measurement_Type(Measurement_Type_ID=361, Measurement_Type_Name="Water Flow IN", Measurement_Type_Variable="FIN", Measurement_Type_Unit="m3/h", Measurement_Type_Segment="Environment"),
            Models.Measurement_Type(Measurement_Type_ID=362, Measurement_Type_Name="Water Flow OUT", Measurement_Type_Variable="FOUT", Measurement_Type_Unit="m3/h", Measurement_Type_Segment="Environment"),
            
            # Water Temperature Measurement Types
            Models.Measurement_Type(Measurement_Type_ID=371, Measurement_Type_Name="Water Temperature IN", Measurement_Type_Variable="TIN", Measurement_Type_Unit="C", Measurement_Type_Segment="Environment"),
            Models.Measurement_Type(Measurement_Type_ID=372, Measurement_Type_Name="Water Temperature OUT", Measurement_Type_Variable="TOUT", Measurement_Type_Unit="C", Measurement_Type_Segment="Environment"),
            
            # Water Level Measurement Types
            Models.Measurement_Type(Measurement_Type_ID=381, Measurement_Type_Name="Water Level", Measurement_Type_Variable="WL", Measurement_Type_Unit="m", Measurement_Type_Segment="Environment"),
            Models.Measurement_Type(Measurement_Type_ID=382, Measurement_Type_Name="Water Level 2", Measurement_Type_Variable="WL2", Measurement_Type_Unit="m", Measurement_Type_Segment="Environment"),
            Models.Measurement_Type(Measurement_Type_ID=383, Measurement_Type_Name="Water Level 3", Measurement_Type_Variable="WL3", Measurement_Type_Unit="m", Measurement_Type_Segment="Environment"),
            Models.Measurement_Type(Measurement_Type_ID=384, Measurement_Type_Name="Water Level 4", Measurement_Type_Variable="WL4", Measurement_Type_Unit="m", Measurement_Type_Segment="Environment"),
            Models.Measurement_Type(Measurement_Type_ID=385, Measurement_Type_Name="Water Level 5", Measurement_Type_Variable="WL5", Measurement_Type_Unit="m", Measurement_Type_Segment="Environment"),

            # Voltage Measurement Types
            Models.Measurement_Type(Measurement_Type_ID=401, Measurement_Type_Name="Phase R Instant Voltage", Measurement_Type_Variable="VR", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=402, Measurement_Type_Name="Phase S Instant Voltage", Measurement_Type_Variable="VS", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=403, Measurement_Type_Name="Phase T Instant Voltage", Measurement_Type_Variable="VT", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=404, Measurement_Type_Name="Phase R RMS Voltage", Measurement_Type_Variable="VR_RMS", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=405, Measurement_Type_Name="Phase S RMS Voltage", Measurement_Type_Variable="VS_RMS", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=406, Measurement_Type_Name="Phase T RMS Voltage", Measurement_Type_Variable="VT_RMS", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=407, Measurement_Type_Name="Phase A RMS Voltage", Measurement_Type_Variable="VA_RMS", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            
            # Harmonic Voltage Measurement Types
            Models.Measurement_Type(Measurement_Type_ID=408, Measurement_Type_Name="Phase R Fundamental Voltage", Measurement_Type_Variable="VR_FUND", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=409, Measurement_Type_Name="Phase S Fundamental Voltage", Measurement_Type_Variable="VS_FUND", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=410, Measurement_Type_Name="Phase T Fundamental Voltage", Measurement_Type_Variable="VT_FUND", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=411, Measurement_Type_Name="Phase R Harmonic[2] Voltage", Measurement_Type_Variable="VR_HARM_2", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=412, Measurement_Type_Name="Phase S Harmonic[2] Voltage", Measurement_Type_Variable="VS_HARM_2", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=413, Measurement_Type_Name="Phase T Harmonic[2] Voltage", Measurement_Type_Variable="VT_HARM_2", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=414, Measurement_Type_Name="Average Harmonic[2] Voltage", Measurement_Type_Variable="VA_HARM_2", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=415, Measurement_Type_Name="Phase R Harmonic[3] Voltage", Measurement_Type_Variable="VR_HARM_3", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=416, Measurement_Type_Name="Phase S Harmonic[3] Voltage", Measurement_Type_Variable="VS_HARM_3", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=417, Measurement_Type_Name="Phase T Harmonic[3] Voltage", Measurement_Type_Variable="VT_HARM_3", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=418, Measurement_Type_Name="Average Harmonic[3] Voltage", Measurement_Type_Variable="VA_HARM_3", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=419, Measurement_Type_Name="Phase R Harmonic[4] Voltage", Measurement_Type_Variable="VR_HARM_4", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=420, Measurement_Type_Name="Phase S Harmonic[4] Voltage", Measurement_Type_Variable="VS_HARM_4", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=421, Measurement_Type_Name="Phase T Harmonic[4] Voltage", Measurement_Type_Variable="VT_HARM_4", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=422, Measurement_Type_Name="Average Harmonic[4] Voltage", Measurement_Type_Variable="VA_HARM_4", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=423, Measurement_Type_Name="Phase R Harmonic[5] Voltage", Measurement_Type_Variable="VR_HARM_5", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=424, Measurement_Type_Name="Phase S Harmonic[5] Voltage", Measurement_Type_Variable="VS_HARM_5", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=425, Measurement_Type_Name="Phase T Harmonic[5] Voltage", Measurement_Type_Variable="VT_HARM_5", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=426, Measurement_Type_Name="Average Harmonic[5] Voltage", Measurement_Type_Variable="VA_HARM_5", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=427, Measurement_Type_Name="Phase R Harmonic[6] Voltage", Measurement_Type_Variable="VR_HARM_6", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=428, Measurement_Type_Name="Phase S Harmonic[6] Voltage", Measurement_Type_Variable="VS_HARM_6", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=429, Measurement_Type_Name="Phase T Harmonic[6] Voltage", Measurement_Type_Variable="VT_HARM_6", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=430, Measurement_Type_Name="Average Harmonic[6] Voltage", Measurement_Type_Variable="VA_HARM_6", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=431, Measurement_Type_Name="Phase R Harmonic[7] Voltage", Measurement_Type_Variable="VR_HARM_7", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=432, Measurement_Type_Name="Phase S Harmonic[7] Voltage", Measurement_Type_Variable="VS_HARM_7", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=433, Measurement_Type_Name="Phase T Harmonic[7] Voltage", Measurement_Type_Variable="VT_HARM_7", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=434, Measurement_Type_Name="Average Harmonic[7] Voltage", Measurement_Type_Variable="VA_HARM_7", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=435, Measurement_Type_Name="Phase R Harmonic[8] Voltage", Measurement_Type_Variable="VR_HARM_8", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=436, Measurement_Type_Name="Phase S Harmonic[8] Voltage", Measurement_Type_Variable="VS_HARM_8", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=437, Measurement_Type_Name="Phase T Harmonic[8] Voltage", Measurement_Type_Variable="VT_HARM_8", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=438, Measurement_Type_Name="Average Harmonic[8] Voltage", Measurement_Type_Variable="VA_HARM_8", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=439, Measurement_Type_Name="Phase R Harmonic[9] Voltage", Measurement_Type_Variable="VR_HARM_9", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=440, Measurement_Type_Name="Phase S Harmonic[9] Voltage", Measurement_Type_Variable="VS_HARM_9", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=441, Measurement_Type_Name="Phase T Harmonic[9] Voltage", Measurement_Type_Variable="VT_HARM_9", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=442, Measurement_Type_Name="Average Harmonic[9] Voltage", Measurement_Type_Variable="VA_HARM_9", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=443, Measurement_Type_Name="Phase R Harmonic[10] Voltage", Measurement_Type_Variable="VR_HARM_10", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=444, Measurement_Type_Name="Phase S Harmonic[10] Voltage", Measurement_Type_Variable="VS_HARM_10", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=445, Measurement_Type_Name="Phase T Harmonic[10] Voltage", Measurement_Type_Variable="VT_HARM_10", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=446, Measurement_Type_Name="Average Harmonic[10] Voltage", Measurement_Type_Variable="VA_HARM_10", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=447, Measurement_Type_Name="Phase R Harmonic[11] Voltage", Measurement_Type_Variable="VR_HARM_11", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=448, Measurement_Type_Name="Phase S Harmonic[11] Voltage", Measurement_Type_Variable="VS_HARM_11", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=449, Measurement_Type_Name="Phase T Harmonic[11] Voltage", Measurement_Type_Variable="VT_HARM_11", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=450, Measurement_Type_Name="Average Harmonic[11] Voltage", Measurement_Type_Variable="VA_HARM_11", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=451, Measurement_Type_Name="Phase R Harmonic[12] Voltage", Measurement_Type_Variable="VR_HARM_12", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=452, Measurement_Type_Name="Phase S Harmonic[12] Voltage", Measurement_Type_Variable="VS_HARM_12", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=453, Measurement_Type_Name="Phase T Harmonic[12] Voltage", Measurement_Type_Variable="VT_HARM_12", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=454, Measurement_Type_Name="Average Harmonic[12] Voltage", Measurement_Type_Variable="VA_HARM_12", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=455, Measurement_Type_Name="Phase R Harmonic[13] Voltage", Measurement_Type_Variable="VR_HARM_13", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=456, Measurement_Type_Name="Phase S Harmonic[13] Voltage", Measurement_Type_Variable="VS_HARM_13", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=457, Measurement_Type_Name="Phase T Harmonic[13] Voltage", Measurement_Type_Variable="VT_HARM_13", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=458, Measurement_Type_Name="Average Harmonic[13] Voltage", Measurement_Type_Variable="VA_HARM_13", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=459, Measurement_Type_Name="Phase R Harmonic[14] Voltage", Measurement_Type_Variable="VR_HARM_14", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=460, Measurement_Type_Name="Phase S Harmonic[14] Voltage", Measurement_Type_Variable="VS_HARM_14", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=461, Measurement_Type_Name="Phase T Harmonic[14] Voltage", Measurement_Type_Variable="VT_HARM_14", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=462, Measurement_Type_Name="Average Harmonic[14] Voltage", Measurement_Type_Variable="VA_HARM_14", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=463, Measurement_Type_Name="Phase R Harmonic[15] Voltage", Measurement_Type_Variable="VR_HARM_15", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=464, Measurement_Type_Name="Phase S Harmonic[15] Voltage", Measurement_Type_Variable="VS_HARM_15", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=465, Measurement_Type_Name="Phase T Harmonic[15] Voltage", Measurement_Type_Variable="VT_HARM_15", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=466, Measurement_Type_Name="Average Harmonic[15] Voltage", Measurement_Type_Variable="VA_HARM_15", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=467, Measurement_Type_Name="Phase R Harmonic[16] Voltage", Measurement_Type_Variable="VR_HARM_16", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=468, Measurement_Type_Name="Phase S Harmonic[16] Voltage", Measurement_Type_Variable="VS_HARM_16", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=469, Measurement_Type_Name="Phase T Harmonic[16] Voltage", Measurement_Type_Variable="VT_HARM_16", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=470, Measurement_Type_Name="Average Harmonic[16] Voltage", Measurement_Type_Variable="VA_HARM_16", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=471, Measurement_Type_Name="Phase R Harmonic[17] Voltage", Measurement_Type_Variable="VR_HARM_17", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=472, Measurement_Type_Name="Phase S Harmonic[17] Voltage", Measurement_Type_Variable="VS_HARM_17", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=473, Measurement_Type_Name="Phase T Harmonic[17] Voltage", Measurement_Type_Variable="VT_HARM_17", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=474, Measurement_Type_Name="Average Harmonic[17] Voltage", Measurement_Type_Variable="VA_HARM_17", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=475, Measurement_Type_Name="Phase R Harmonic[18] Voltage", Measurement_Type_Variable="VR_HARM_18", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=476, Measurement_Type_Name="Phase S Harmonic[18] Voltage", Measurement_Type_Variable="VS_HARM_18", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=477, Measurement_Type_Name="Phase T Harmonic[18] Voltage", Measurement_Type_Variable="VT_HARM_18", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=478, Measurement_Type_Name="Average Harmonic[18] Voltage", Measurement_Type_Variable="VA_HARM_18", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=479, Measurement_Type_Name="Phase R Harmonic[19] Voltage", Measurement_Type_Variable="VR_HARM_19", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=480, Measurement_Type_Name="Phase S Harmonic[19] Voltage", Measurement_Type_Variable="VS_HARM_19", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=481, Measurement_Type_Name="Phase T Harmonic[19] Voltage", Measurement_Type_Variable="VT_HARM_19", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=482, Measurement_Type_Name="Average Harmonic[19] Voltage", Measurement_Type_Variable="VA_HARM_19", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=483, Measurement_Type_Name="Phase R Harmonic[20] Voltage", Measurement_Type_Variable="VR_HARM_20", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=484, Measurement_Type_Name="Phase S Harmonic[20] Voltage", Measurement_Type_Variable="VS_HARM_20", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=485, Measurement_Type_Name="Phase T Harmonic[20] Voltage", Measurement_Type_Variable="VT_HARM_20", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=486, Measurement_Type_Name="Average Harmonic[20] Voltage", Measurement_Type_Variable="VA_HARM_20", Measurement_Type_Unit="V", Measurement_Type_Segment="Energy"),

            # Current Measurement Types
            Models.Measurement_Type(Measurement_Type_ID=501, Measurement_Type_Name="Phase R Instant Current", Measurement_Type_Variable="IR", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=502, Measurement_Type_Name="Phase S Instant Current", Measurement_Type_Variable="IS", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=503, Measurement_Type_Name="Phase T Instant Current", Measurement_Type_Variable="IT", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=504, Measurement_Type_Name="Phase R RMS Current", Measurement_Type_Variable="IR_RMS", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=505, Measurement_Type_Name="Phase S RMS Current", Measurement_Type_Variable="IS_RMS", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=506, Measurement_Type_Name="Phase T RMS Current", Measurement_Type_Variable="IT_RMS", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=507, Measurement_Type_Name="Phase A RMS Current", Measurement_Type_Variable="IA_RMS", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),

            # Harmonic Current Measurement Types
            Models.Measurement_Type(Measurement_Type_ID=508, Measurement_Type_Name="Phase R Fundamental Current", Measurement_Type_Variable="IR_FUND", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=509, Measurement_Type_Name="Phase S Fundamental Current", Measurement_Type_Variable="IS_FUND", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=510, Measurement_Type_Name="Phase T Fundamental Current", Measurement_Type_Variable="IT_FUND", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=511, Measurement_Type_Name="Phase R Harmonic[2] Current", Measurement_Type_Variable="IR_HARM_2", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=512, Measurement_Type_Name="Phase S Harmonic[2] Current", Measurement_Type_Variable="IS_HARM_2", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=513, Measurement_Type_Name="Phase T Harmonic[2] Current", Measurement_Type_Variable="IT_HARM_2", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=514, Measurement_Type_Name="Average Harmonic[2] Current", Measurement_Type_Variable="IA_HARM_2", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=515, Measurement_Type_Name="Phase R Harmonic[3] Current", Measurement_Type_Variable="IR_HARM_3", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=516, Measurement_Type_Name="Phase S Harmonic[3] Current", Measurement_Type_Variable="IS_HARM_3", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=517, Measurement_Type_Name="Phase T Harmonic[3] Current", Measurement_Type_Variable="IT_HARM_3", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=518, Measurement_Type_Name="Average Harmonic[3] Current", Measurement_Type_Variable="IA_HARM_3", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=519, Measurement_Type_Name="Phase R Harmonic[4] Current", Measurement_Type_Variable="IR_HARM_4", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=520, Measurement_Type_Name="Phase S Harmonic[4] Current", Measurement_Type_Variable="IS_HARM_4", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=521, Measurement_Type_Name="Phase T Harmonic[4] Current", Measurement_Type_Variable="IT_HARM_4", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=522, Measurement_Type_Name="Average Harmonic[4] Current", Measurement_Type_Variable="IA_HARM_4", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=523, Measurement_Type_Name="Phase R Harmonic[5] Current", Measurement_Type_Variable="IR_HARM_5", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=524, Measurement_Type_Name="Phase S Harmonic[5] Current", Measurement_Type_Variable="IS_HARM_5", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=525, Measurement_Type_Name="Phase T Harmonic[5] Current", Measurement_Type_Variable="IT_HARM_5", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=526, Measurement_Type_Name="Average Harmonic[5] Current", Measurement_Type_Variable="IA_HARM_5", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=527, Measurement_Type_Name="Phase R Harmonic[6] Current", Measurement_Type_Variable="IR_HARM_6", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=528, Measurement_Type_Name="Phase S Harmonic[6] Current", Measurement_Type_Variable="IS_HARM_6", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=529, Measurement_Type_Name="Phase T Harmonic[6] Current", Measurement_Type_Variable="IT_HARM_6", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=530, Measurement_Type_Name="Average Harmonic[6] Current", Measurement_Type_Variable="IA_HARM_6", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=531, Measurement_Type_Name="Phase R Harmonic[7] Current", Measurement_Type_Variable="IR_HARM_7", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=532, Measurement_Type_Name="Phase S Harmonic[7] Current", Measurement_Type_Variable="IS_HARM_7", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=533, Measurement_Type_Name="Phase T Harmonic[7] Current", Measurement_Type_Variable="IT_HARM_7", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=534, Measurement_Type_Name="Average Harmonic[7] Current", Measurement_Type_Variable="IA_HARM_7", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=535, Measurement_Type_Name="Phase R Harmonic[8] Current", Measurement_Type_Variable="IR_HARM_8", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=536, Measurement_Type_Name="Phase S Harmonic[8] Current", Measurement_Type_Variable="IS_HARM_8", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=537, Measurement_Type_Name="Phase T Harmonic[8] Current", Measurement_Type_Variable="IT_HARM_8", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=538, Measurement_Type_Name="Average Harmonic[8] Current", Measurement_Type_Variable="IA_HARM_8", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=539, Measurement_Type_Name="Phase R Harmonic[9] Current", Measurement_Type_Variable="IR_HARM_9", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=540, Measurement_Type_Name="Phase S Harmonic[9] Current", Measurement_Type_Variable="IS_HARM_9", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=541, Measurement_Type_Name="Phase T Harmonic[9] Current", Measurement_Type_Variable="IT_HARM_9", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=542, Measurement_Type_Name="Average Harmonic[9] Current", Measurement_Type_Variable="IA_HARM_9", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=543, Measurement_Type_Name="Phase R Harmonic[10] Current", Measurement_Type_Variable="IR_HARM_10", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=544, Measurement_Type_Name="Phase S Harmonic[10] Current", Measurement_Type_Variable="IS_HARM_10", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=545, Measurement_Type_Name="Phase T Harmonic[10] Current", Measurement_Type_Variable="IT_HARM_10", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=546, Measurement_Type_Name="Average Harmonic[10] Current", Measurement_Type_Variable="IA_HARM_10", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=547, Measurement_Type_Name="Phase R Harmonic[11] Current", Measurement_Type_Variable="IR_HARM_11", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=548, Measurement_Type_Name="Phase S Harmonic[11] Current", Measurement_Type_Variable="IS_HARM_11", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=549, Measurement_Type_Name="Phase T Harmonic[11] Current", Measurement_Type_Variable="IT_HARM_11", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=550, Measurement_Type_Name="Average Harmonic[11] Current", Measurement_Type_Variable="IA_HARM_11", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=551, Measurement_Type_Name="Phase R Harmonic[12] Current", Measurement_Type_Variable="IR_HARM_12", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=552, Measurement_Type_Name="Phase S Harmonic[12] Current", Measurement_Type_Variable="IS_HARM_12", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=553, Measurement_Type_Name="Phase T Harmonic[12] Current", Measurement_Type_Variable="IT_HARM_12", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=554, Measurement_Type_Name="Average Harmonic[12] Current", Measurement_Type_Variable="IA_HARM_12", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=555, Measurement_Type_Name="Phase R Harmonic[13] Current", Measurement_Type_Variable="IR_HARM_13", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=556, Measurement_Type_Name="Phase S Harmonic[13] Current", Measurement_Type_Variable="IS_HARM_13", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=557, Measurement_Type_Name="Phase T Harmonic[13] Current", Measurement_Type_Variable="IT_HARM_13", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=558, Measurement_Type_Name="Average Harmonic[13] Current", Measurement_Type_Variable="IA_HARM_13", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=559, Measurement_Type_Name="Phase R Harmonic[14] Current", Measurement_Type_Variable="IR_HARM_14", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=560, Measurement_Type_Name="Phase S Harmonic[14] Current", Measurement_Type_Variable="IS_HARM_14", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=561, Measurement_Type_Name="Phase T Harmonic[14] Current", Measurement_Type_Variable="IT_HARM_14", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=562, Measurement_Type_Name="Average Harmonic[14] Current", Measurement_Type_Variable="IA_HARM_14", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=563, Measurement_Type_Name="Phase R Harmonic[15] Current", Measurement_Type_Variable="IR_HARM_15", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=564, Measurement_Type_Name="Phase S Harmonic[15] Current", Measurement_Type_Variable="IS_HARM_15", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=565, Measurement_Type_Name="Phase T Harmonic[15] Current", Measurement_Type_Variable="IT_HARM_15", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=566, Measurement_Type_Name="Average Harmonic[15] Current", Measurement_Type_Variable="IA_HARM_15", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=567, Measurement_Type_Name="Phase R Harmonic[16] Current", Measurement_Type_Variable="IR_HARM_16", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=568, Measurement_Type_Name="Phase S Harmonic[16] Current", Measurement_Type_Variable="IS_HARM_16", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=569, Measurement_Type_Name="Phase T Harmonic[16] Current", Measurement_Type_Variable="IT_HARM_16", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=570, Measurement_Type_Name="Average Harmonic[16] Current", Measurement_Type_Variable="IA_HARM_16", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=571, Measurement_Type_Name="Phase R Harmonic[17] Current", Measurement_Type_Variable="IR_HARM_17", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=572, Measurement_Type_Name="Phase S Harmonic[17] Current", Measurement_Type_Variable="IS_HARM_17", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=573, Measurement_Type_Name="Phase T Harmonic[17] Current", Measurement_Type_Variable="IT_HARM_17", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=574, Measurement_Type_Name="Average Harmonic[17] Current", Measurement_Type_Variable="IA_HARM_17", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=575, Measurement_Type_Name="Phase R Harmonic[18] Current", Measurement_Type_Variable="IR_HARM_18", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=576, Measurement_Type_Name="Phase S Harmonic[18] Current", Measurement_Type_Variable="IS_HARM_18", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=577, Measurement_Type_Name="Phase T Harmonic[18] Current", Measurement_Type_Variable="IT_HARM_18", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=578, Measurement_Type_Name="Average Harmonic[18] Current", Measurement_Type_Variable="IA_HARM_18", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=579, Measurement_Type_Name="Phase R Harmonic[19] Current", Measurement_Type_Variable="IR_HARM_19", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=580, Measurement_Type_Name="Phase S Harmonic[19] Current", Measurement_Type_Variable="IS_HARM_19", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=581, Measurement_Type_Name="Phase T Harmonic[19] Current", Measurement_Type_Variable="IT_HARM_19", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=582, Measurement_Type_Name="Average Harmonic[19] Current", Measurement_Type_Variable="IA_HARM_19", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=583, Measurement_Type_Name="Phase R Harmonic[20] Current", Measurement_Type_Variable="IR_HARM_20", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=584, Measurement_Type_Name="Phase S Harmonic[20] Current", Measurement_Type_Variable="IS_HARM_20", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=585, Measurement_Type_Name="Phase T Harmonic[20] Current", Measurement_Type_Variable="IT_HARM_20", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=586, Measurement_Type_Name="Average Harmonic[20] Current", Measurement_Type_Variable="IA_HARM_20", Measurement_Type_Unit="A", Measurement_Type_Segment="Energy"),

            # Power Measurement Types
            Models.Measurement_Type(Measurement_Type_ID=601, Measurement_Type_Name="Phase R Active Power", Measurement_Type_Variable="PR", Measurement_Type_Unit="W", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=602, Measurement_Type_Name="Phase S Active Power", Measurement_Type_Variable="PS", Measurement_Type_Unit="W", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=603, Measurement_Type_Name="Phase T Active Power", Measurement_Type_Variable="PT", Measurement_Type_Unit="W", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=604, Measurement_Type_Name="Average Active Power", Measurement_Type_Variable="PA", Measurement_Type_Unit="W", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=605, Measurement_Type_Name="Phase R Reactive Power", Measurement_Type_Variable="QR", Measurement_Type_Unit="VAR", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=606, Measurement_Type_Name="Phase S Reactive Power", Measurement_Type_Variable="QS", Measurement_Type_Unit="VAR", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=607, Measurement_Type_Name="Phase T Reactive Power", Measurement_Type_Variable="QT", Measurement_Type_Unit="VAR", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=608, Measurement_Type_Name="Average Reactive Power", Measurement_Type_Variable="QA", Measurement_Type_Unit="VAR", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=609, Measurement_Type_Name="Phase R Apparent Power", Measurement_Type_Variable="SR", Measurement_Type_Unit="VA", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=610, Measurement_Type_Name="Phase S Apparent Power", Measurement_Type_Variable="SS", Measurement_Type_Unit="VA", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=611, Measurement_Type_Name="Phase T Apparent Power", Measurement_Type_Variable="ST", Measurement_Type_Unit="VA", Measurement_Type_Segment="Energy"),
            Models.Measurement_Type(Measurement_Type_ID=612, Measurement_Type_Name="Average Apparent Power", Measurement_Type_Variable="SA", Measurement_Type_Unit="VA", Measurement_Type_Segment="Energy"),


            # GSM Parameters
            Models.Measurement_Type(Measurement_Type_ID=901, Measurement_Type_Name="GSM TAC ID", Measurement_Type_Variable="TAC", Measurement_Type_Unit="-", Measurement_Type_Segment="GSM"),
            Models.Measurement_Type(Measurement_Type_ID=902, Measurement_Type_Name="GSM LAC ID", Measurement_Type_Variable="LAC", Measurement_Type_Unit="-", Measurement_Type_Segment="GSM"),
            Models.Measurement_Type(Measurement_Type_ID=903, Measurement_Type_Name="GSM Cell ID", Measurement_Type_Variable="Cell_ID", Measurement_Type_Unit="-", Measurement_Type_Segment="GSM"),

            # Location Parameters
            Models.Measurement_Type(Measurement_Type_ID=1001, Measurement_Type_Name="Latitude", Measurement_Type_Variable="Latitude", Measurement_Type_Unit="°", Measurement_Type_Segment="Location"),
            Models.Measurement_Type(Measurement_Type_ID=1002, Measurement_Type_Name="Longitude", Measurement_Type_Variable="Longitude", Measurement_Type_Unit="°", Measurement_Type_Segment="Location"),

        ]

        # Add Record to DataBase
        for record in Model_Records:

            # Check for Existing Record
            Query_Record = DB_Module.query(Models.Measurement_Type).filter(Models.Measurement_Type.Measurement_Type_ID==(record.Measurement_Type_ID)).first()

            # Record Not Found
            if not Query_Record:

                # Add Record to DataBase
                DB_Module.add(record)
        
        # Commit DataBase
        DB_Module.commit()

        # Log Message
        Log.Terminal_Log("INFO", f"Measurement_Type Table Default Values Updated")

    except Exception as e:

        # Log Message
        Log.Terminal_Log("ERROR", f"An error occurred while adding Module_Model Table : {e}")

# Call Functions
def Value_Update():

    # Update Module_Type Table
    Module_Type_Initial_Values()

    # Update GSM_Manufacturer Table
    GSM_Manufacturer_Initial_Values()

    # Update GSM_Model Table
    GSM_Model_Initial_Values()

    # Update Measurement_Type Table
    Measurement_Type_Initial_Values()
