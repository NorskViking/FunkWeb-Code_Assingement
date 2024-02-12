#!/bin/python3
# Python Weather Forecast
import datetime as dt
import requests
import json

BASE_URL = "https://api.met.no/weatherapi/locationforecast/2.0/compact?"
USER_AGENT = {"User-Agent": "Weather_ForeCast jorgen@funkweb.org"}
CITY = "Oslo"
OSLO = "lat=59.91273&lon=10.74609"

url = BASE_URL

response = requests.get(url).json()
print(response.status_code)

data = response.text

x = '{"name":"Jørgen", "age":31, "city":"Oslo}'
# parse_json = json.loads(x)

print(x)
