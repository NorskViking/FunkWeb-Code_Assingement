#!/bin/python3
# Python Weather Forecast
import datetime as dt
import requests
import json
import simplejson

# Open JSON data over Norwegian cities
nor_cities = open('nor.json')
# Convert JSON object to dict
nor_data = json.load(nor_cities)
# Close JSON file
nor_cities.close()

OSLO = ""
# Get coordinates for Oslo
for i in nor_data:
    if i['city'] == 'Oslo':
        OSLO = "lat="+str(i['lat'])+"&lon="+str(i['lon'])


BASE_URL = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?"
USER_AGENT = {"User-Agent": "Weather_ForeCast jorgen@funkweb.org"}

url = BASE_URL+OSLO

weather_data = requests.get(url, headers=USER_AGENT).json()

#print(first_req)

# Store weather_data in local JSON file.
with open('weather.json', 'w') as json_file:
    json_file.write(simplejson.dumps(weather_data, indent=4))

#response = requests.get(url).json()
#print(response.status_code)

#data = response.text