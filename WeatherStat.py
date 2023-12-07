# Library Includes
from Functions import Log, Handler, Functions
from Setup import Schema
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from astral import LocationInfo, moon
from astral.sun import sun
from astral.moon import moonrise, moonset
from datetime import date, datetime, timezone
import python_weather
import pytz

# Set Timezone
Local_Timezone = pytz.timezone("Europe/Istanbul")

# Define WeatherStat Object
WeatherStat = FastAPI(version="01.00.00", title="WeatherStat")

# API Boot Sequence
@WeatherStat.on_event("startup")
async def Startup_Event():

	# Log Message
	Log.Terminal_Log("DEBUG", f"WeatherStat API Started {datetime.now()}")
	Log.Terminal_Log("DEBUG", f"*************************************************")

# API ShutDown Sequence
@WeatherStat.on_event("shutdown")
async def Shutdown_event():

	# Log Message
	Log.Terminal_Log("DEBUG", f"WeatherStat API Shutdown {datetime.now()}")

# App Get Method
@WeatherStat.get("/WeatherStat/{ID}", response_model=Schema.Response_Model, status_code=status.HTTP_200_OK)
@WeatherStat.get("/WeatherStat/{ID}/", response_model=Schema.Response_Model, status_code=status.HTTP_200_OK)
async def WeatherStat_Mobile_App_Root(request: Request, ID: str) -> Schema.Response_Model:

	# Log Message
	Log.Terminal_Log("INFO", f"New app request: {request.client.host}")

	# Get Last Update Time and Update to Local Time
	Last_Update = Handler.Get_Device_Last_Connection(ID)
	Last_Update = Last_Update.astimezone(Local_Timezone)

	# Control for Device
	if Last_Update is not None:

		# Set Device
		Device_JSON = Schema.Device_Response(
			Device_ID = ID, 
			LastUpdate = Last_Update.strftime("%Y-%m-%d %H:%M:%S"), 
			TTU = (30 - int((datetime.now(timezone.utc) - Last_Update).total_seconds() / 60))
		)

		# Parse Measurement
		# -----------------

		# Get AT Data
		AT_JSON = None
		AT_Data = Handler.Get_Payload_Measurement(ID, "AT")
		if AT_Data is not None: 

			# Check if Data is Up to Date
			AT_UptoDate = Functions.Check_Up_to_Date(str(AT_Data.Last_Time))

			# Parse Data
			AT_JSON = Schema.Payload_Value_Response(
				Last = AT_Data.Last_Value, 
				Change = AT_Data.Trend, 
				Max = AT_Data.Max, 
				Max_Time = AT_Data.Max_Time, 
				Min = AT_Data.Min, 
				Min_Time = AT_Data.Min_Time, 
				UpToDate = AT_UptoDate
			)

		# Get AT_FL Data
		AT_FL_JSON = None
		AT_FL_Data = Handler.Get_Payload_Measurement(ID, "AT_FL")
		if AT_FL_Data is not None: 

			# Check if Data is Up to Date
			AT_FL_UptoDate = Functions.Check_Up_to_Date(str(AT_FL_Data.Last_Time))

			# Parse Data
			AT_FL_JSON = Schema.Payload_Value_Response(
				Last = AT_FL_Data.Last_Value, 
				Change = AT_FL_Data.Trend, 
				UpToDate = AT_FL_UptoDate
			)

		# Get AT_Dew Data
		AT_Dew_JSON = None
		AT_Dew_Data = Handler.Get_Payload_Measurement(ID, "AT_Dew")
		if AT_Dew_Data is not None: 

			# Check if Data is Up to Date
			AT_Dew_UptoDate = Functions.Check_Up_to_Date(str(AT_Dew_Data.Last_Time))

			# Parse Data
			AT_Dew_JSON = Schema.Payload_Value_Response(
				Last = AT_Dew_Data.Last_Value, 
				Change = AT_Dew_Data.Trend, 
				UpToDate = AT_Dew_UptoDate
			)

		# Get AH Data
		AH_JSON = None
		AH_Data = Handler.Get_Payload_Measurement(ID, "AH")
		if AH_Data is not None: 
			
			# Check if Data is Up to Date
			AH_UptoDate = Functions.Check_Up_to_Date(str(AH_Data.Last_Time))

			# Parse Data
			AH_JSON = Schema.Payload_Value_Response(
				Last = AH_Data.Last_Value, 
				Change = AH_Data.Trend, 
				UpToDate = AH_UptoDate
			)
	
		# Get AP Data
		AP_JSON = None
		AP_Data = Handler.Get_Payload_Measurement(ID, "AP")
		if AP_Data is not None: 

			# Check if Data is Up to Date
			AP_UptoDate = Functions.Check_Up_to_Date(str(AP_Data.Last_Time))

			# Parse Data
			AP_JSON = Schema.Payload_Value_Response(
				Last = AP_Data.Last_Value, 
				Change = AP_Data.Trend, 
				UpToDate = AP_UptoDate
			)

		# Get R Data
		R_JSON = None
		R_Data = Handler.Get_Rain_Totals(ID)
		if R_Data is not None:

			# Parse Rain Data
			R_JSON = Schema.Rain_Response(
				R_1 = R_Data.R_1, 
				R_24 = R_Data.R_24, 
				R_48 = R_Data.R_48, 
				R_168 = R_Data.R_168
			)

		# Get WS Data
		WS_JSON = None
		WS_Data = Handler.Get_Payload_Measurement(ID, "WS")
		if WS_Data is not None: 
			
			# Check if Data is Up to Date
			WS_UptoDate = Functions.Check_Up_to_Date(str(WS_Data.Last_Time))

			# Parse Data
			WS_JSON = Schema.Payload_Value_Response(
				Last = WS_Data.Last_Value, 
				UpToDate = WS_UptoDate
			)

		# Get WD Data
		WD_JSON = None
		WD_Data = Handler.Get_Payload_Measurement(ID, "WD")
		if WD_Data is not None: 

			# Check if Data is Up to Date
			WD_UptoDate = Functions.Check_Up_to_Date(str(WD_Data.Last_Time))

			# Parse Data		
			WD_JSON = Schema.Payload_Value_Response(
				Last = WD_Data.Last_Value, 
				UpToDate = WD_UptoDate
			)

		# Get UV Data
		UV_JSON = None
		UV_Data = Handler.Get_Payload_Measurement(ID, "UV")
		if UV_Data is not None: 

			# Check if Data is Up to Date
			UV_UptoDate = Functions.Check_Up_to_Date(str(UV_Data.Last_Time))

			# Parse Data			
			UV_JSON = Schema.Payload_Value_Response(
				Last = UV_Data.Last_Value, 
				UpToDate = UV_UptoDate
			)

		# Set ST Model
		ST_JSON = None
		ST_10_Data = Handler.Get_Payload_Measurement(ID, "ST0")
		ST_20_Data = Handler.Get_Payload_Measurement(ID, "ST1")
		ST_30_Data = Handler.Get_Payload_Measurement(ID, "ST2")
		ST_40_Data = Handler.Get_Payload_Measurement(ID, "ST3")
		ST_50_Data = Handler.Get_Payload_Measurement(ID, "ST4")
		ST_60_Data = Handler.Get_Payload_Measurement(ID, "ST5")
		ST_70_Data = Handler.Get_Payload_Measurement(ID, "ST6")
		ST_80_Data = Handler.Get_Payload_Measurement(ID, "ST7")
		ST_90_Data = Handler.Get_Payload_Measurement(ID, "ST8")
		ST_100_Data = Handler.Get_Payload_Measurement(ID, "ST9")
		if ST_10_Data is not None or ST_20_Data is not None or ST_30_Data is not None or ST_40_Data is not None or ST_50_Data is not None or ST_60_Data is not None or ST_70_Data is not None or ST_80_Data is not None or ST_90_Data is not None or ST_100_Data is not None:

			# Get ST_10 Data
			ST_10_JSON = None
			if ST_10_Data is not None: 

				# Check if Data is Up to Date
				ST_10_UptoDate = Functions.Check_Up_to_Date(str(ST_10_Data.Last_Time))

				# Parse Data
				ST_10_JSON = Schema.Payload_Value_Response(
					Last = ST_10_Data.Last_Value, 
					Change = ST_10_Data.Trend, 
					UpToDate = ST_10_UptoDate
				)

			# Get ST_20 Data
			ST_20_JSON = None
			if ST_20_Data is not None: 

				# Check if Data is Up to Date
				ST_20_UptoDate = Functions.Check_Up_to_Date(str(ST_20_Data.Last_Time))

				# Parse Data
				ST_20_JSON = Schema.Payload_Value_Response(
					Last = ST_20_Data.Last_Value, 
					Change = ST_20_Data.Trend, 
					UpToDate = ST_20_UptoDate
				)

			# Get ST_30 Data
			ST_30_JSON = None
			if ST_30_Data is not None: 

				# Check if Data is Up to Date
				ST_30_UptoDate = Functions.Check_Up_to_Date(str(ST_30_Data.Last_Time))

				# Parse Data
				ST_30_JSON = Schema.Payload_Value_Response(
					Last = ST_30_Data.Last_Value, 
					Change = ST_30_Data.Trend, 
					UpToDate = ST_30_UptoDate
				)

			# Get ST_40 Data
			ST_40_JSON = None
			if ST_40_Data is not None: 

				# Check if Data is Up to Date
				ST_40_UptoDate = Functions.Check_Up_to_Date(str(ST_40_Data.Last_Time))

				# Parse Data
				ST_40_JSON = Schema.Payload_Value_Response(
					Last = ST_40_Data.Last_Value, 
					Change = ST_40_Data.Trend, 
					UpToDate = ST_40_UptoDate
				)

			# Get ST_50 Data
			ST_50_JSON = None
			if ST_50_Data is not None: 

				# Check if Data is Up to Date
				ST_50_UptoDate = Functions.Check_Up_to_Date(str(ST_50_Data.Last_Time))

				# Parse Data
				ST_50_JSON = Schema.Payload_Value_Response(
					Last = ST_50_Data.Last_Value, 
					Change = ST_50_Data.Trend, 
					UpToDate = ST_50_UptoDate
				)

			# Get ST_60 Data
			ST_60_JSON = None
			if ST_60_Data is not None: 

				# Check if Data is Up to Date
				ST_60_UptoDate = Functions.Check_Up_to_Date(str(ST_60_Data.Last_Time))

				# Parse Data
				ST_60_JSON = Schema.Payload_Value_Response(
					Last = ST_60_Data.Last_Value, 
					Change = ST_60_Data.Trend, 
					UpToDate = ST_60_UptoDate
				)

			# Get ST_70 Data
			ST_70_JSON = None
			if ST_70_Data is not None: 

				# Check if Data is Up to Date
				ST_70_UptoDate = Functions.Check_Up_to_Date(str(ST_70_Data.Last_Time))

				# Parse Data
				ST_70_JSON = Schema.Payload_Value_Response(
					Last = ST_70_Data.Last_Value, 
					Change = ST_70_Data.Trend, 
					UpToDate = ST_70_UptoDate
				)

			# Get ST_80 Data
			ST_80_JSON = None
			if ST_80_Data is not None: 

				# Check if Data is Up to Date
				ST_80_UptoDate = Functions.Check_Up_to_Date(str(ST_80_Data.Last_Time))

				# Parse Data
				ST_80_JSON = Schema.Payload_Value_Response(
					Last = ST_80_Data.Last_Value, 
					Change = ST_80_Data.Trend, 
					UpToDate = ST_80_UptoDate
				)

			# Get ST_90 Data
			ST_90_JSON = None
			if ST_90_Data is not None: 

				# Check if Data is Up to Date
				ST_90_UptoDate = Functions.Check_Up_to_Date(str(ST_90_Data.Last_Time))

				# Parse Data
				ST_90_JSON = Schema.Payload_Value_Response(
					Last = ST_90_Data.Last_Value, 
					Change = ST_90_Data.Trend, 
					UpToDate = ST_90_UptoDate
				)

			# Get ST_100 Data
			ST_100_JSON = None
			if ST_100_Data is not None: 

				# Check if Data is Up to Date
				ST_100_UptoDate = Functions.Check_Up_to_Date(str(ST_100_Data.Last_Time))

				# Parse Data
				ST_100_JSON = Schema.Payload_Value_Response(
					Last = ST_100_Data.Last_Value, 
					Change = ST_100_Data.Trend, 
					UpToDate = ST_100_UptoDate
				)

			# Set ST Model
			ST_JSON = Schema.ST(
				ST_10 = ST_10_JSON, 
				ST_20 = ST_20_JSON, 
				ST_30 = ST_30_JSON, 
				ST_40 = ST_40_JSON, 
				ST_50 = ST_50_JSON, 
				ST_60 = ST_60_JSON, 
				ST_70 = ST_70_JSON, 
				ST_80 = ST_80_JSON, 
				ST_90 = ST_90_JSON, 
				ST_100 = ST_100_JSON
			)

		# Set Weather Model
		WeatherStat_JSON = Schema.WeatherStat(
			AT = AT_JSON, 
			AT_FL = AT_FL_JSON, 
			AT_Dew = AT_Dew_JSON, 
			AH = AH_JSON, 
			AP = AP_JSON, 
			R = R_JSON, 
			WS = WS_JSON, 
			WD = WD_JSON, 
			UV = UV_JSON, 
			ST = ST_JSON
		)

		# Get BV Data
		BV_JSON = None
		BIV_Data = Handler.Get_Parameter_Measurement(ID, "B_IV")
		if BIV_Data is not None: 
			
			# Check if Data is Up to Date
			BIV_UptoDate = Functions.Check_Up_to_Date(str(BIV_Data.Last_Time))
			
			# Parse Data
			BV_JSON = Schema.Payload_Value_Response(
				Last = BIV_Data.Last_Value, 
				Change = BIV_Data.Trend, 
				UpToDate = BIV_UptoDate
			)
		
		# Get BSOC Data
		BSOC_JSON = None
		BSOC_Data = Handler.Get_Parameter_Measurement(ID, "B_SOC")
		if BSOC_Data is not None:

			# Check if Data is Up to Date
			BSOC_UptoDate = Functions.Check_Up_to_Date(str(BSOC_Data.Last_Time))

			# Parse Data
			BSOC_JSON = Schema.Payload_Value_Response(
				Last = BSOC_Data.Last_Value, 
				Change = BSOC_Data.Trend, 
				UpToDate = BSOC_UptoDate
			)

		# Set Battery Model
		Power_JSON = Schema.Power(
			BV = BV_JSON, 
			SOC = BSOC_JSON
		)

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

		# Parse Sun Model
		Sun_JSON = Schema.Sun_Response(
			Sunrise=Sun_Rise_Time, 
			Sunset=Sun_Set_Time
		)

		# Parse Moon Model
		Moon_JSON = Schema.Moon_Response(
			Moonrise=Moon_Rise_Time, 
			Moonset=Moon_Set_Time, 
			Phase=Moon_Phase
		)

		# Set Astronomy Model
		Astronomy_JSON = Schema.Astronomy(
			Sun=Sun_JSON, 
			Moon=Moon_JSON
		)

		# Set Response Model
		Response_Message = Schema.Response_Model(
			Device = Device_JSON, 
			WeatherStat = WeatherStat_JSON, 
			Power = Power_JSON, 
			Astronomy = Astronomy_JSON
		)

		# Send Response
		return Response_Message

	# Device Not Found
	else:

		# Message Status Code
		Message_Status_Code = status.HTTP_404_NOT_FOUND

		# Message Content
		Message_Content = {"Event": status.HTTP_404_NOT_FOUND}

		# Send Response
		return JSONResponse(
			status_code=Message_Status_Code, 
			content=Message_Content
		)

# Forecast Get Method
@WeatherStat.get("/WeatherStat/Forecast/{City}", response_model=Schema.Full_Forecast, status_code=status.HTTP_200_OK)
@WeatherStat.get("/WeatherStat/Forecast/{City}/", response_model=Schema.Full_Forecast, status_code=status.HTTP_200_OK)
async def Mobile_Forcast_Root(request: Request, City: str) -> Schema.Full_Forecast:

	# Declare Forecast Data
	async with python_weather.Client(unit=python_weather.METRIC) as client:

		# Set Forecast Location
		weather = await client.get(City)

		# Set Forecast Model
		Full_Forecast_Model = Schema.Full_Forecast(ForecastList=[])

		# Get Forecast Data
		for forecast in weather.forecasts:
			for hourly in forecast.hourly:

				# Set Forecast Model
				Single_Forecast = Schema.Forecast(
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
