#!/bin/python3

from Weather_Forecast import Place, Forecast
import json
import datetime as dt

USER_AGENT = "Weather_ForeCast jorgen@funkweb.org"

nor_cities = open("./data/nor.json")
# Convert JSON object to dict
nor_data = json.load(nor_cities)
# Close JSON file
nor_cities.close()
norwegian_citys = []

oslo = None

for city in nor_data:
    norwegian_citys.append(Place(city["city"], float(city["lat"]), float(city["lon"])))
    if city["city"] == "Oslo":
        oslo = Place(city["city"], float(city["lat"]), float(city["lon"]))


base_forecast: Forecast = Forecast(oslo, USER_AGENT)
base_forecast.update()

wind = False
rain = False
temperatur = True

def tomorrows_forecast(forecast: Forecast):
    """Get and print tomorrows Weather_forecast
        Get tomorrows date.
        Print the temperature for each hour thru the tomorrow. 
    """
    tomorrow = dt.date.today() + dt.timedelta(days=1)
    
    tomorrows_intervals = forecast.data.intervals_for(tomorrow)
    
    print(f"Værmelding for {forecast.place.name}, {tomorrow}:")
    for interval in tomorrows_intervals:
        start_time = interval.start_time
        temp_data = interval.variables["air_temperature"]
        rain_data = interval.variables["precipitation_amount"]
        wind_data = interval.variables["wind_speed"]
        hour_min = str(start_time.time())[0:5] #Only get hours and minutes
        print(f"kl. {hour_min}:", end=" ")
        if temperatur:
            print(f"Temperatur: {temp_data.value}{temp_data.units}", end=" ")
        if rain:
            print(f"Regn: {rain_data.value}{rain_data.units}", end=" ")
        if wind:
            print(f"Vind: {wind_data.value}{wind_data.units}", end=" ")
        print("")
            
        
def median_temperature(forecast: Forecast):
    """Get the median temperature in intervals of 6 hours for tomorrow"""
    #Get tomorrows date
    tomorrow = dt.date.today() + dt.timedelta(days=1)
    #Set start time for the first interval to be 'YYYY-MM-DD 00:00:00'
    start_of_day = dt.datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day, hour=00, minute=0, second=0)
    #Set end time of first interval be 'YYYY-MM-DD 06:00:00'
    first_interval = dt.datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day, hour=6, minute=0, second=0)
    #Set end time of second interval to be 'YYYY-MM-DD 12:00:00'
    secound_interval = dt.datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day, hour=12, minute=0, second=0)
    #Set end time of third interval to be 'YYYY-MM-DD 18:00:00'
    third_interval = dt.datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day, hour=18, minute=0, second=0)
    #Set end time of fourth interval to be 'YYYY-MM-DD+1 00:00:00'
    fourth_interval = dt.datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day+1, hour=00, minute=0, second=0)
    
    first_median: float = 0.0
    second_median: float = 0.0
    third_median: float = 0.0
    fourth_median: float = 0.0
    
    tomorrows_intervals = forecast.data.intervals_for(tomorrow)
    for interval in tomorrows_intervals:
        if interval.start_time >= start_of_day and interval.end_time <= first_interval:
            first_median += float(interval.variables["air_temperature"].value)
        elif interval.start_time >= first_interval and interval.end_time <= secound_interval:
            second_median += float(interval.variables["air_temperature"].value)
        elif interval.start_time >= secound_interval and interval.end_time <= third_interval:
            third_median += float(interval.variables["air_temperature"].value)
        elif interval.start_time >= third_interval and interval.end_time <= fourth_interval:
            fourth_median += float(interval.variables["air_temperature"].value)
    #Get the median temperatur for each time interval
    first_median = round(first_median/6, 2)
    second_median = round(second_median/6, 2)
    third_median = round(third_median/6, 2)
    fourth_median = round(fourth_median/6, 2)
    
    print(
        f"Snitt-temperatur for {forecast.place.name}, {tomorrow}:\n"
        f"00:00-06:00: {first_median} celsius\n"
        f"06:00-12:00: {second_median} celsius\n"
        f"12:00-18:00: {third_median} celsius\n"
        f"18:00-00:00: {fourth_median} celsius\n"
        )

user_input = 1

while user_input != "avslutt":
    forecast = base_forecast
    forecast.update()
    print("Værdata v0.0.2\n"
        f"'imorgen' for morgendagens værdata\n"
        f"'snitt' for morgendagens snitt-temperatur\n"
        f"'by' for å finne værmelding for gitt bynavn\n"
        f"'vind' for å inkludere/eksludere vindstyrke i værmelding\n"
        f"'regn' for å inkludere/eksludere regnmengde i værmelding\n"
        f"'temperatur' for å inkludere/eksludere temperatur i værmelding\n"
        f"For å avlsutte, skriv avslutt")
    user_input = input()
    if user_input == "imorgen":
        tomorrows_forecast(forecast)
    if user_input == "snitt":
        median_temperature(forecast)
    if user_input == "by":
        city_name = input("Bynavn:")
        """Tried using a function for changing the forecast object
            Forecast object got changed to str object and broke the program.
        """
        for city in norwegian_citys:
            if city.name == city_name:
                base_forecast = Forecast(city, USER_AGENT)
    if user_input == "vind":
        wind = not wind
    if user_input == "regn":
        rain = not rain
    if user_input == "temperatur":
        temperatur = not temperatur                