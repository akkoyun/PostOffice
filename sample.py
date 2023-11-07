# import the module
import python_weather

import asyncio
import os

async def getweather():

    # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
    async with python_weather.Client(unit=python_weather.METRIC) as client:

        # fetch a weather forecast from a city
        weather = await client.get('Konya')
        
        ID = 1

        # get the weather forecast for a few days
        for forecast in weather.forecasts:
            for hourly in forecast.hourly:
                print(f'{ID} - {forecast.date} {hourly.time}: {hourly.temperature}, {hourly.cloud_cover}, {hourly.wind_speed}, {hourly.wind_direction}, {hourly.chances_of_rain}, {hourly.chances_of_snow}')
                ID+=1




if __name__ == '__main__':
  
  asyncio.run(getweather())