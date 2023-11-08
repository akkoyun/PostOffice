# Setup Root Path
import sys
sys.path.append('/root/PostOffice/')

# Import Packages
from fastapi import Request, status, APIRouter
from fastapi.responses import JSONResponse
from Setup import Schema, App_Schema
from Functions import Log, Kafka, Handler
from Setup.Config import APP_Settings
from astral import LocationInfo, moon
from astral.sun import sun
from astral.moon import moonrise, moonset
from datetime import date, datetime, timezone
import python_weather
import pytz

# Set Timezone
Local_Timezone = pytz.timezone("Europe/Istanbul")

# Define FastAPI Object
PostOffice_WeatherStat = APIRouter()

# IoT Post Method
@PostOffice_WeatherStat.post("", status_code=status.HTTP_201_CREATED, include_in_schema=False)
@PostOffice_WeatherStat.post("/", status_code=status.HTTP_201_CREATED)
async def WeatherStat_POST(request: Request, Data: Schema.Data_Pack):

	# Log Message
	Log.Terminal_Log("INFO", f"New Data Recieved from: {request.client.host}")

	# Set headers
	RAW_Header = [
		("Command", bytes(Data.Info.Command, 'utf-8')), 
		("Device_ID", bytes(Data.Info.ID, 'utf-8')),
		("Device_Time", bytes(Data.Info.TimeStamp, 'utf-8')), 
		("Device_IP", bytes(request.client.host, 'utf-8')),
		("Size", bytes(request.headers['content-length'], 'utf-8')),
	]
	
	# Send to Kafka Topic
	Kafka.Send_To_Topic("RAW", Data.json(), RAW_Header)

	# Log Message
	Log.Terminal_Log("INFO", f"****************************************")

	# Message Status Code
	Message_Status_Code = status.HTTP_200_OK

	# Message Content
	Message_Content = {"Event": status.HTTP_200_OK}

	# Headers
	Message_Headers = {"server": APP_Settings.SERVER_NAME}

	# Send Response
	return JSONResponse(status_code=Message_Status_Code, content=Message_Content, headers=Message_Headers)

# App Get Method
@PostOffice_WeatherStat.get("/{ID}", response_model=App_Schema.Model, status_code=status.HTTP_200_OK)
@PostOffice_WeatherStat.get("/{ID}/", response_model=App_Schema.Model, status_code=status.HTTP_200_OK)
async def Mobile_App_Root(request: Request, ID: str) -> App_Schema.Model:

	# Log Message
	Log.Terminal_Log("INFO", f"New Data Recieved from: {request.client.host}")

	# Get Last Update Time
	Last_Update = Handler.Get_Device_Last_Connection(ID)

	# Control for Device
	if Last_Update is not None:

		# Get Now Time
		Now = datetime.now(timezone.utc)

		# Calculate Minute Difference with Now
		TTU = 30 - int((Now - Last_Update).total_seconds() / 60)

		# Get Device Time
		# ---------------

		# Change Last Update Time to Local Time
		Last_Update = Last_Update.astimezone(Local_Timezone)

		# Set Device
		Device = App_Schema.Device(Device_ID = ID, LastUpdate = Last_Update.strftime("%Y-%m-%d %H:%M:%S"), TTU = TTU)

		# Get Last Data
		# --------------

		# Get Last Data
		AT_Data = Handler.Get_WeatherStat_Measurement(ID, "AT")
		AT_FL_Data = Handler.Get_WeatherStat_Measurement(ID, "AT_FL")
		AT_Dew_Data = Handler.Get_WeatherStat_Measurement(ID, "AT_Dew")
		AH_Data = Handler.Get_WeatherStat_Measurement(ID, "AH")
		AP_Data = Handler.Get_WeatherStat_Measurement(ID, "AP")
		WS_Data = Handler.Get_WeatherStat_Measurement(ID, "WS")
		WD_Data = Handler.Get_WeatherStat_Measurement(ID, "WD")
		UV_Data = Handler.Get_WeatherStat_Measurement(ID, "UV")
		ST0_Data = Handler.Get_WeatherStat_Measurement(ID, "ST0")
		ST2_Data = Handler.Get_WeatherStat_Measurement(ID, "ST2")
		ST5_Data = Handler.Get_WeatherStat_Measurement(ID, "ST5")
		ST8_Data = Handler.Get_WeatherStat_Measurement(ID, "ST8")

		# Parse Measurement
		# -----------------

		# Parse AT Data
		AT = None
		if AT_Data is not None:
			
			# Parse Max AT Data
			MAX_AT = App_Schema.MaxAT(Value=AT_Data.Max, Time=AT_Data.Max_Time)
			
			# Parse Min AT Data
			MIN_AT = App_Schema.MinAT(Value=AT_Data.Min, Time=AT_Data.Min_Time)
			
			# Parse AT Data
			AT = App_Schema.AT(Value=AT_Data.Last_Value, Change=AT_Data.Trend, AT_FL=AT_FL_Data.Last_Value, AT_Dew=AT_Dew_Data.Last_Value, Max_AT = MAX_AT, Min_AT = MIN_AT)

		# Parse AH Data
		AH = None
		if AH_Data is not None:

			# Parse AH Data
			AH = App_Schema.AH(Value=AH_Data.Last_Value, Change=AH_Data.Trend)

		# Parse AP Data
		AP = None
		if AP_Data is not None:
			
			# Parse AP Data
			AP = App_Schema.AP(Value=AP_Data.Last_Value, Change=AP_Data.Trend)

		# Parse Wind Data
		W = None
		if WS_Data is not None and WD_Data is not None:
			
			# Parse Wind Data
			Wind = App_Schema.W(WS=WS_Data.Last_Value, WD=WD_Data.Last_Value, Change=WS_Data.Trend)

		# Parse UV Data
		UV = None
		if UV_Data is not None:

			# Parse UV Data
			UV = App_Schema.UV(Value=UV_Data.Last_Value, Change=UV_Data.Trend)

		# Parse ST0 Data
		ST0 = None
		if ST0_Data is not None:
			
			# Parse ST0 Data
			ST0 = App_Schema.ST_10(Value=ST0_Data.Last_Value, Change=ST0_Data.Trend)
		
		# Parse ST2 Data
		ST2 = None
		if ST2_Data is not None:

			# Parse ST2 Data
			ST2 = App_Schema.ST_30(Value=ST2_Data.Last_Value, Change=ST2_Data.Trend)
		
		# Parse ST5 Data
		ST5 = None
		if ST5_Data is not None:
			
			# Parse ST5 Data
			ST5 = App_Schema.ST_60(Value=ST5_Data.Last_Value, Change=ST5_Data.Trend)
		
		# Parse ST8 Data
		ST8 = None
		if ST8_Data is not None:

			# Parse ST8 Data
			ST8 = App_Schema.ST_90(Value=ST8_Data.Last_Value, Change=ST8_Data.Trend)
		
		# Parse ST Model
		ST = None
		ST = App_Schema.ST(ST_10=ST0, ST_30=ST2, ST_60=ST5, ST_90=ST8)

		# Set Sun and Moon
		# -----------------

		# Set Object
		Sun = None
		Moon = None

		# Set Location
		City = LocationInfo(name='Konya', region='Turkey', timezone='Europe/Istanbul', latitude=37.8716, longitude=32.4846)

		# Set Sun
		Sun_State = sun(City.observer, date.today())

		# Get Sun Rise Time
		try:
			Sun_Rise_Time = Sun_State["sunrise"].astimezone(Local_Timezone).strftime("%Y-%m-%d %H:%M:%S")
		except ValueError as e:
			Sun_Rise_Time = None

		# Get Sun Set Time
		try:
			Sun_Set_Time = Sun_State["sunset"].astimezone(Local_Timezone).strftime("%Y-%m-%d %H:%M:%S")
		except ValueError as e:
			Sun_Set_Time = None

		# Parse Sun Model
		Sun = App_Schema.Sun(Sunrise=Sun_Rise_Time, Sunset=Sun_Set_Time)

		# Get Moon Rise Time
		try:
			Moon_Rise_Time = moonrise(City, date.today()).astimezone(Local_Timezone).strftime("%Y-%m-%d %H:%M:%S")
		except ValueError as e:
			Moon_Rise_Time = None

		# Get Moon Set Time
		try:
			Moon_Set_Time = moonset(City, date.today()).astimezone(Local_Timezone).strftime("%Y-%m-%d %H:%M:%S")
		except ValueError as e:
			Moon_Set_Time = None

		# Get Moon Phase
		try:
			Moon_Phase = moon.phase(date.today())
		except ValueError as e:
			Moon_Phase = None

		# Parse Moon Model
		Moon = App_Schema.Moon(Moonrise=Moon_Rise_Time, Moonset=Moon_Set_Time, Phase=Moon_Phase)
		
		# Parse Device Model
		# ------------------

		# Set Model
		Response_Message = App_Schema.Model(Device = Device, AT = AT, AH = AH, AP = AP, W = Wind, UV = UV, ST = ST, Sun = Sun, Moon = Moon)

		# Set Response
		return Response_Message
	
	# Device Not Found
	else:

		# Message Status Code
		Message_Status_Code = status.HTTP_404_NOT_FOUND

		# Message Content
		Message_Content = {"Event": status.HTTP_404_NOT_FOUND}

		# Headers
		Message_Headers = {"server": APP_Settings.SERVER_NAME}

		# Send Response
		return JSONResponse(status_code=Message_Status_Code, content=Message_Content, headers=Message_Headers)

# Forecast Get Method
@PostOffice_WeatherStat.get("/{ID}/Forecast", response_model=App_Schema.Full_Forecast, status_code=status.HTTP_200_OK)
@PostOffice_WeatherStat.get("/{ID}/Forecast/", response_model=App_Schema.Full_Forecast, status_code=status.HTTP_200_OK)
async def Mobile_Forcast_Root(request: Request, ID: str) -> App_Schema.Full_Forecast:

	# Declare Forecast Data
	async with python_weather.Client(unit=python_weather.METRIC) as client:

		# Set Forecast Location
		weather = await client.get('Konya')

		# Set Forecast Model
		Full_Forecast_Model = App_Schema.Full_Forecast(ForecastList=[])

		# Get Forecast Data
		for forecast in weather.forecasts:
			for hourly in forecast.hourly:
					
				# Set Forecast Model
				Single_Forecast = App_Schema.Forecast(
					Date=str(forecast.date), 
					Time=str(hourly.time), 
					AT=int(hourly.temperature), 
					CC=int(hourly.cloud_cover), 
					WS=int(hourly.wind_speed), 
					WD=str(hourly.wind_direction), 
					CoR=int(hourly.chances_of_rain), 
					CoS=int(hourly.chances_of_snow)
				)

				# Append Forecast
				Full_Forecast_Model.ForecastList.append(Single_Forecast)

	# Set Response
	return Full_Forecast_Model
