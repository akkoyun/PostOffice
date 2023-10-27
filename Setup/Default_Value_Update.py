# Setup Library
import sys
sys.path.append('/root/PostOffice/')

# Library Includes
from Setup import Database, Models, Log
import pandas as pd

# Define DB
DB_Module = Database.SessionLocal()

# GSM Module Manufacturer Add Record
def GSM_Manufacturer_Initial_Values():
    
    try:

        # Define MNC Records
        Manufacturer_Records = [
            Models.Manufacturer(Manufacturer_ID=0, Manufacturer="Unknown"),
            Models.Manufacturer(Manufacturer_ID=1, Manufacturer="Telit"),
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
            Models.Model(Model_ID=0, Model="Unknown"),
            Models.Model(Model_ID=1, Model="GE910 QUAD"),
            Models.Model(Model_ID=2, Model="GE910 QUAD V3"),
            Models.Model(Model_ID=3, Model="GE910 GNSS"),
            Models.Model(Model_ID=4, Model="LE910 S1 EA"),
            Models.Model(Model_ID=5, Model="LE910 S1 EAG"),
            Models.Model(Model_ID=6, Model="LE910 R1 EU"),
            Models.Model(Model_ID=7, Model="LE910 C1 EUX"),
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
            Models.Measurement_Type(Type_ID=0, Decription="Unknown", Variable="", Unit="", Segment=0),

            # Battery Measurement Types
            Models.Measurement_Type(Type_ID=101, Decription="Battery Instant Voltage", Variable="IV", Unit="V", Segment=1),
            Models.Measurement_Type(Type_ID=102, Decription="Battery Average Current", Variable="AC", Unit="mA", Segment=1),
            Models.Measurement_Type(Type_ID=103, Decription="Battery State of Charge", Variable="SOC", Unit="%", Segment=1),
            Models.Measurement_Type(Type_ID=104, Decription="Battery Temperature", Variable="T", Unit="C", Segment=1),
            Models.Measurement_Type(Type_ID=105, Decription="Battery Full Capacity", Variable="FB", Unit="mAh", Segment=1),
            Models.Measurement_Type(Type_ID=106, Decription="Battery Instant Capacity", Variable="IB", Unit="mAh", Segment=1),
            Models.Measurement_Type(Type_ID=107, Decription="Battery Charge State", Variable="Charge", Unit="-", Segment=1),

            # Environment Measurement Types
            Models.Measurement_Type(Type_ID=311, Decription="Air Temperature", Variable="AT", Unit="C", Segment=2),
            Models.Measurement_Type(Type_ID=312, Decription="Air Humidity", Variable="AH", Unit="%", Segment=2),
            Models.Measurement_Type(Type_ID=313, Decription="Air Pressure", Variable="AP", Unit="hPa", Segment=2),
            Models.Measurement_Type(Type_ID=314, Decription="UV Index", Variable="UV", Unit="-", Segment=2),
            Models.Measurement_Type(Type_ID=315, Decription="Visual Light", Variable="VL", Unit="Lux", Segment=2),
            Models.Measurement_Type(Type_ID=316, Decription="Infrared Light", Variable="IL", Unit="Lux", Segment=2),
            
            # Soil Temperature Measurement Types
            Models.Measurement_Type(Type_ID=320, Decription="Soil Temperature 0", Variable="ST0", Unit="C", Segment=2),
            Models.Measurement_Type(Type_ID=321, Decription="Soil Temperature 1", Variable="ST1", Unit="C", Segment=2),
            Models.Measurement_Type(Type_ID=322, Decription="Soil Temperature 2", Variable="ST2", Unit="C", Segment=2),
            Models.Measurement_Type(Type_ID=323, Decription="Soil Temperature 3", Variable="ST3", Unit="C", Segment=2),
            Models.Measurement_Type(Type_ID=324, Decription="Soil Temperature 4", Variable="ST4", Unit="C", Segment=2),
            Models.Measurement_Type(Type_ID=325, Decription="Soil Temperature 5", Variable="ST5", Unit="C", Segment=2),
            Models.Measurement_Type(Type_ID=326, Decription="Soil Temperature 6", Variable="ST6", Unit="C", Segment=2),
            Models.Measurement_Type(Type_ID=327, Decription="Soil Temperature 7", Variable="ST7", Unit="C", Segment=2),
            Models.Measurement_Type(Type_ID=328, Decription="Soil Temperature 8", Variable="ST8", Unit="C", Segment=2),
            Models.Measurement_Type(Type_ID=329, Decription="Soil Temperature 9", Variable="ST9", Unit="C", Segment=2),
            
            # Rain Measurement Types
            Models.Measurement_Type(Type_ID=331, Decription="Rain", Variable="R", Unit="m/sn", Segment=2),
            
            # Wind Measurement Types
            Models.Measurement_Type(Type_ID=341, Decription="Wind Speed", Variable="WS", Unit="m/sn", Segment=2),
            Models.Measurement_Type(Type_ID=342, Decription="Wind Direction", Variable="WD", Unit="Degree", Segment=2),
            
            # Water Pressure Measurement Types
            Models.Measurement_Type(Type_ID=351, Decription="Water Pressure IN", Variable="PIN", Unit="Bar", Segment=2),
            Models.Measurement_Type(Type_ID=352, Decription="Water Pressure OUT", Variable="POUT", Unit="Bar", Segment=2),
            
            # Water Flow Measurement Types
            Models.Measurement_Type(Type_ID=361, Decription="Water Flow IN", Variable="FIN", Unit="m3/h", Segment=2),
            Models.Measurement_Type(Type_ID=362, Decription="Water Flow OUT", Variable="FOUT", Unit="m3/h", Segment=2),
            
            # Water Temperature Measurement Types
            Models.Measurement_Type(Type_ID=371, Decription="Water Temperature IN", Variable="TIN", Unit="C", Segment=2),
            Models.Measurement_Type(Type_ID=372, Decription="Water Temperature OUT", Variable="TOUT", Unit="C", Segment=2),
            
            # Water Level Measurement Types
            Models.Measurement_Type(Type_ID=381, Decription="Water Level", Variable="WL", Unit="m", Segment=2),
            Models.Measurement_Type(Type_ID=382, Decription="Water Level 2", Variable="WL2", Unit="m", Segment=2),
            Models.Measurement_Type(Type_ID=383, Decription="Water Level 3", Variable="WL3", Unit="m", Segment=2),
            Models.Measurement_Type(Type_ID=384, Decription="Water Level 4", Variable="WL4", Unit="m", Segment=2),
            Models.Measurement_Type(Type_ID=385, Decription="Water Level 5", Variable="WL5", Unit="m", Segment=2),

            # Voltage Measurement Types
            Models.Measurement_Type(Type_ID=401, Decription="Phase R Instant Voltage", Variable="VR", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=402, Decription="Phase S Instant Voltage", Variable="VS", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=403, Decription="Phase T Instant Voltage", Variable="VT", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=404, Decription="Phase R RMS Voltage", Variable="VR_RMS", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=405, Decription="Phase S RMS Voltage", Variable="VS_RMS", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=406, Decription="Phase T RMS Voltage", Variable="VT_RMS", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=407, Decription="Phase A RMS Voltage", Variable="VA_RMS", Unit="V", Segment=3),
            
            # Harmonic Voltage Measurement Types
            Models.Measurement_Type(Type_ID=408, Decription="Phase R Fundamental Voltage", Variable="VR_FUND", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=409, Decription="Phase S Fundamental Voltage", Variable="VS_FUND", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=410, Decription="Phase T Fundamental Voltage", Variable="VT_FUND", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=411, Decription="Phase R Harmonic[2] Voltage", Variable="VR_HARM_2", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=412, Decription="Phase S Harmonic[2] Voltage", Variable="VS_HARM_2", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=413, Decription="Phase T Harmonic[2] Voltage", Variable="VT_HARM_2", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=414, Decription="Average Harmonic[2] Voltage", Variable="VA_HARM_2", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=415, Decription="Phase R Harmonic[3] Voltage", Variable="VR_HARM_3", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=416, Decription="Phase S Harmonic[3] Voltage", Variable="VS_HARM_3", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=417, Decription="Phase T Harmonic[3] Voltage", Variable="VT_HARM_3", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=418, Decription="Average Harmonic[3] Voltage", Variable="VA_HARM_3", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=419, Decription="Phase R Harmonic[4] Voltage", Variable="VR_HARM_4", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=420, Decription="Phase S Harmonic[4] Voltage", Variable="VS_HARM_4", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=421, Decription="Phase T Harmonic[4] Voltage", Variable="VT_HARM_4", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=422, Decription="Average Harmonic[4] Voltage", Variable="VA_HARM_4", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=423, Decription="Phase R Harmonic[5] Voltage", Variable="VR_HARM_5", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=424, Decription="Phase S Harmonic[5] Voltage", Variable="VS_HARM_5", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=425, Decription="Phase T Harmonic[5] Voltage", Variable="VT_HARM_5", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=426, Decription="Average Harmonic[5] Voltage", Variable="VA_HARM_5", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=427, Decription="Phase R Harmonic[6] Voltage", Variable="VR_HARM_6", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=428, Decription="Phase S Harmonic[6] Voltage", Variable="VS_HARM_6", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=429, Decription="Phase T Harmonic[6] Voltage", Variable="VT_HARM_6", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=430, Decription="Average Harmonic[6] Voltage", Variable="VA_HARM_6", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=431, Decription="Phase R Harmonic[7] Voltage", Variable="VR_HARM_7", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=432, Decription="Phase S Harmonic[7] Voltage", Variable="VS_HARM_7", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=433, Decription="Phase T Harmonic[7] Voltage", Variable="VT_HARM_7", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=434, Decription="Average Harmonic[7] Voltage", Variable="VA_HARM_7", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=435, Decription="Phase R Harmonic[8] Voltage", Variable="VR_HARM_8", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=436, Decription="Phase S Harmonic[8] Voltage", Variable="VS_HARM_8", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=437, Decription="Phase T Harmonic[8] Voltage", Variable="VT_HARM_8", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=438, Decription="Average Harmonic[8] Voltage", Variable="VA_HARM_8", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=439, Decription="Phase R Harmonic[9] Voltage", Variable="VR_HARM_9", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=440, Decription="Phase S Harmonic[9] Voltage", Variable="VS_HARM_9", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=441, Decription="Phase T Harmonic[9] Voltage", Variable="VT_HARM_9", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=442, Decription="Average Harmonic[9] Voltage", Variable="VA_HARM_9", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=443, Decription="Phase R Harmonic[10] Voltage", Variable="VR_HARM_10", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=444, Decription="Phase S Harmonic[10] Voltage", Variable="VS_HARM_10", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=445, Decription="Phase T Harmonic[10] Voltage", Variable="VT_HARM_10", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=446, Decription="Average Harmonic[10] Voltage", Variable="VA_HARM_10", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=447, Decription="Phase R Harmonic[11] Voltage", Variable="VR_HARM_11", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=448, Decription="Phase S Harmonic[11] Voltage", Variable="VS_HARM_11", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=449, Decription="Phase T Harmonic[11] Voltage", Variable="VT_HARM_11", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=450, Decription="Average Harmonic[11] Voltage", Variable="VA_HARM_11", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=451, Decription="Phase R Harmonic[12] Voltage", Variable="VR_HARM_12", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=452, Decription="Phase S Harmonic[12] Voltage", Variable="VS_HARM_12", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=453, Decription="Phase T Harmonic[12] Voltage", Variable="VT_HARM_12", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=454, Decription="Average Harmonic[12] Voltage", Variable="VA_HARM_12", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=455, Decription="Phase R Harmonic[13] Voltage", Variable="VR_HARM_13", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=456, Decription="Phase S Harmonic[13] Voltage", Variable="VS_HARM_13", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=457, Decription="Phase T Harmonic[13] Voltage", Variable="VT_HARM_13", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=458, Decription="Average Harmonic[13] Voltage", Variable="VA_HARM_13", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=459, Decription="Phase R Harmonic[14] Voltage", Variable="VR_HARM_14", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=460, Decription="Phase S Harmonic[14] Voltage", Variable="VS_HARM_14", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=461, Decription="Phase T Harmonic[14] Voltage", Variable="VT_HARM_14", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=462, Decription="Average Harmonic[14] Voltage", Variable="VA_HARM_14", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=463, Decription="Phase R Harmonic[15] Voltage", Variable="VR_HARM_15", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=464, Decription="Phase S Harmonic[15] Voltage", Variable="VS_HARM_15", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=465, Decription="Phase T Harmonic[15] Voltage", Variable="VT_HARM_15", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=466, Decription="Average Harmonic[15] Voltage", Variable="VA_HARM_15", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=467, Decription="Phase R Harmonic[16] Voltage", Variable="VR_HARM_16", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=468, Decription="Phase S Harmonic[16] Voltage", Variable="VS_HARM_16", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=469, Decription="Phase T Harmonic[16] Voltage", Variable="VT_HARM_16", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=470, Decription="Average Harmonic[16] Voltage", Variable="VA_HARM_16", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=471, Decription="Phase R Harmonic[17] Voltage", Variable="VR_HARM_17", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=472, Decription="Phase S Harmonic[17] Voltage", Variable="VS_HARM_17", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=473, Decription="Phase T Harmonic[17] Voltage", Variable="VT_HARM_17", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=474, Decription="Average Harmonic[17] Voltage", Variable="VA_HARM_17", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=475, Decription="Phase R Harmonic[18] Voltage", Variable="VR_HARM_18", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=476, Decription="Phase S Harmonic[18] Voltage", Variable="VS_HARM_18", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=477, Decription="Phase T Harmonic[18] Voltage", Variable="VT_HARM_18", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=478, Decription="Average Harmonic[18] Voltage", Variable="VA_HARM_18", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=479, Decription="Phase R Harmonic[19] Voltage", Variable="VR_HARM_19", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=480, Decription="Phase S Harmonic[19] Voltage", Variable="VS_HARM_19", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=481, Decription="Phase T Harmonic[19] Voltage", Variable="VT_HARM_19", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=482, Decription="Average Harmonic[19] Voltage", Variable="VA_HARM_19", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=483, Decription="Phase R Harmonic[20] Voltage", Variable="VR_HARM_20", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=484, Decription="Phase S Harmonic[20] Voltage", Variable="VS_HARM_20", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=485, Decription="Phase T Harmonic[20] Voltage", Variable="VT_HARM_20", Unit="V", Segment=3),
            Models.Measurement_Type(Type_ID=486, Decription="Average Harmonic[20] Voltage", Variable="VA_HARM_20", Unit="V", Segment=3),

            # Current Measurement Types
            Models.Measurement_Type(Type_ID=501, Decription="Phase R Instant Current", Variable="IR", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=502, Decription="Phase S Instant Current", Variable="IS", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=503, Decription="Phase T Instant Current", Variable="IT", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=504, Decription="Phase R RMS Current", Variable="IR_RMS", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=505, Decription="Phase S RMS Current", Variable="IS_RMS", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=506, Decription="Phase T RMS Current", Variable="IT_RMS", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=507, Decription="Phase A RMS Current", Variable="IA_RMS", Unit="A", Segment=3),

            # Harmonic Current Measurement Types
            Models.Measurement_Type(Type_ID=508, Decription="Phase R Fundamental Current", Variable="IR_FUND", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=509, Decription="Phase S Fundamental Current", Variable="IS_FUND", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=510, Decription="Phase T Fundamental Current", Variable="IT_FUND", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=511, Decription="Phase R Harmonic[2] Current", Variable="IR_HARM_2", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=512, Decription="Phase S Harmonic[2] Current", Variable="IS_HARM_2", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=513, Decription="Phase T Harmonic[2] Current", Variable="IT_HARM_2", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=514, Decription="Average Harmonic[2] Current", Variable="IA_HARM_2", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=515, Decription="Phase R Harmonic[3] Current", Variable="IR_HARM_3", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=516, Decription="Phase S Harmonic[3] Current", Variable="IS_HARM_3", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=517, Decription="Phase T Harmonic[3] Current", Variable="IT_HARM_3", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=518, Decription="Average Harmonic[3] Current", Variable="IA_HARM_3", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=519, Decription="Phase R Harmonic[4] Current", Variable="IR_HARM_4", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=520, Decription="Phase S Harmonic[4] Current", Variable="IS_HARM_4", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=521, Decription="Phase T Harmonic[4] Current", Variable="IT_HARM_4", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=522, Decription="Average Harmonic[4] Current", Variable="IA_HARM_4", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=523, Decription="Phase R Harmonic[5] Current", Variable="IR_HARM_5", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=524, Decription="Phase S Harmonic[5] Current", Variable="IS_HARM_5", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=525, Decription="Phase T Harmonic[5] Current", Variable="IT_HARM_5", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=526, Decription="Average Harmonic[5] Current", Variable="IA_HARM_5", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=527, Decription="Phase R Harmonic[6] Current", Variable="IR_HARM_6", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=528, Decription="Phase S Harmonic[6] Current", Variable="IS_HARM_6", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=529, Decription="Phase T Harmonic[6] Current", Variable="IT_HARM_6", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=530, Decription="Average Harmonic[6] Current", Variable="IA_HARM_6", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=531, Decription="Phase R Harmonic[7] Current", Variable="IR_HARM_7", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=532, Decription="Phase S Harmonic[7] Current", Variable="IS_HARM_7", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=533, Decription="Phase T Harmonic[7] Current", Variable="IT_HARM_7", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=534, Decription="Average Harmonic[7] Current", Variable="IA_HARM_7", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=535, Decription="Phase R Harmonic[8] Current", Variable="IR_HARM_8", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=536, Decription="Phase S Harmonic[8] Current", Variable="IS_HARM_8", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=537, Decription="Phase T Harmonic[8] Current", Variable="IT_HARM_8", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=538, Decription="Average Harmonic[8] Current", Variable="IA_HARM_8", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=539, Decription="Phase R Harmonic[9] Current", Variable="IR_HARM_9", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=540, Decription="Phase S Harmonic[9] Current", Variable="IS_HARM_9", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=541, Decription="Phase T Harmonic[9] Current", Variable="IT_HARM_9", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=542, Decription="Average Harmonic[9] Current", Variable="IA_HARM_9", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=543, Decription="Phase R Harmonic[10] Current", Variable="IR_HARM_10", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=544, Decription="Phase S Harmonic[10] Current", Variable="IS_HARM_10", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=545, Decription="Phase T Harmonic[10] Current", Variable="IT_HARM_10", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=546, Decription="Average Harmonic[10] Current", Variable="IA_HARM_10", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=547, Decription="Phase R Harmonic[11] Current", Variable="IR_HARM_11", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=548, Decription="Phase S Harmonic[11] Current", Variable="IS_HARM_11", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=549, Decription="Phase T Harmonic[11] Current", Variable="IT_HARM_11", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=550, Decription="Average Harmonic[11] Current", Variable="IA_HARM_11", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=551, Decription="Phase R Harmonic[12] Current", Variable="IR_HARM_12", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=552, Decription="Phase S Harmonic[12] Current", Variable="IS_HARM_12", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=553, Decription="Phase T Harmonic[12] Current", Variable="IT_HARM_12", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=554, Decription="Average Harmonic[12] Current", Variable="IA_HARM_12", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=555, Decription="Phase R Harmonic[13] Current", Variable="IR_HARM_13", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=556, Decription="Phase S Harmonic[13] Current", Variable="IS_HARM_13", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=557, Decription="Phase T Harmonic[13] Current", Variable="IT_HARM_13", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=558, Decription="Average Harmonic[13] Current", Variable="IA_HARM_13", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=559, Decription="Phase R Harmonic[14] Current", Variable="IR_HARM_14", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=560, Decription="Phase S Harmonic[14] Current", Variable="IS_HARM_14", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=561, Decription="Phase T Harmonic[14] Current", Variable="IT_HARM_14", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=562, Decription="Average Harmonic[14] Current", Variable="IA_HARM_14", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=563, Decription="Phase R Harmonic[15] Current", Variable="IR_HARM_15", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=564, Decription="Phase S Harmonic[15] Current", Variable="IS_HARM_15", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=565, Decription="Phase T Harmonic[15] Current", Variable="IT_HARM_15", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=566, Decription="Average Harmonic[15] Current", Variable="IA_HARM_15", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=567, Decription="Phase R Harmonic[16] Current", Variable="IR_HARM_16", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=568, Decription="Phase S Harmonic[16] Current", Variable="IS_HARM_16", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=569, Decription="Phase T Harmonic[16] Current", Variable="IT_HARM_16", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=570, Decription="Average Harmonic[16] Current", Variable="IA_HARM_16", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=571, Decription="Phase R Harmonic[17] Current", Variable="IR_HARM_17", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=572, Decription="Phase S Harmonic[17] Current", Variable="IS_HARM_17", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=573, Decription="Phase T Harmonic[17] Current", Variable="IT_HARM_17", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=574, Decription="Average Harmonic[17] Current", Variable="IA_HARM_17", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=575, Decription="Phase R Harmonic[18] Current", Variable="IR_HARM_18", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=576, Decription="Phase S Harmonic[18] Current", Variable="IS_HARM_18", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=577, Decription="Phase T Harmonic[18] Current", Variable="IT_HARM_18", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=578, Decription="Average Harmonic[18] Current", Variable="IA_HARM_18", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=579, Decription="Phase R Harmonic[19] Current", Variable="IR_HARM_19", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=580, Decription="Phase S Harmonic[19] Current", Variable="IS_HARM_19", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=581, Decription="Phase T Harmonic[19] Current", Variable="IT_HARM_19", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=582, Decription="Average Harmonic[19] Current", Variable="IA_HARM_19", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=583, Decription="Phase R Harmonic[20] Current", Variable="IR_HARM_20", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=584, Decription="Phase S Harmonic[20] Current", Variable="IS_HARM_20", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=585, Decription="Phase T Harmonic[20] Current", Variable="IT_HARM_20", Unit="A", Segment=3),
            Models.Measurement_Type(Type_ID=586, Decription="Average Harmonic[20] Current", Variable="IA_HARM_20", Unit="A", Segment=3),

            # Power Measurement Types
            Models.Measurement_Type(Type_ID=601, Decription="Phase R Active Power", Variable="PR", Unit="W", Segment=3),
            Models.Measurement_Type(Type_ID=602, Decription="Phase S Active Power", Variable="PS", Unit="W", Segment=3),
            Models.Measurement_Type(Type_ID=603, Decription="Phase T Active Power", Variable="PT", Unit="W", Segment=3),
            Models.Measurement_Type(Type_ID=604, Decription="Average Active Power", Variable="PA", Unit="W", Segment=3),
            Models.Measurement_Type(Type_ID=605, Decription="Phase R Reactive Power", Variable="QR", Unit="VAR", Segment=3),
            Models.Measurement_Type(Type_ID=606, Decription="Phase S Reactive Power", Variable="QS", Unit="VAR", Segment=3),
            Models.Measurement_Type(Type_ID=607, Decription="Phase T Reactive Power", Variable="QT", Unit="VAR", Segment=3),
            Models.Measurement_Type(Type_ID=608, Decription="Average Reactive Power", Variable="QA", Unit="VAR", Segment=3),
            Models.Measurement_Type(Type_ID=609, Decription="Phase R Apparent Power", Variable="SR", Unit="VA", Segment=3),
            Models.Measurement_Type(Type_ID=610, Decription="Phase S Apparent Power", Variable="SS", Unit="VA", Segment=3),
            Models.Measurement_Type(Type_ID=611, Decription="Phase T Apparent Power", Variable="ST", Unit="VA", Segment=3),
            Models.Measurement_Type(Type_ID=612, Decription="Average Apparent Power", Variable="SA", Unit="VA", Segment=3),


            # GSM Parameters
            Models.Measurement_Type(Type_ID=901, Decription="GSM TAC ID", Variable="TAC", Unit="-", Segment=4),
            Models.Measurement_Type(Type_ID=902, Decription="GSM LAC ID", Variable="LAC", Unit="-", Segment=4),
            Models.Measurement_Type(Type_ID=903, Decription="GSM Cell ID", Variable="Cell_ID", Unit="-", Segment=4),

            # Location Parameters
            Models.Measurement_Type(Type_ID=1001, Decription="Latitude", Variable="Latitude", Unit="°", Segment=5),
            Models.Measurement_Type(Type_ID=1002, Decription="Longitude", Variable="Longitude", Unit="°", Segment=5),

        ]

        # Add Record to DataBase
        for record in Model_Records:

            # Check for Existing Record
            Query_Record = DB_Module.query(Models.Measurement_Type).filter(Models.Measurement_Type.Type_ID==(record.Type_ID)).first()

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

    # Update GSM_Manufacturer Table
    GSM_Manufacturer_Initial_Values()

    # Update GSM_Model Table
    GSM_Model_Initial_Values()

    # Update Measurement_Type Table
    Measurement_Type_Initial_Values()
