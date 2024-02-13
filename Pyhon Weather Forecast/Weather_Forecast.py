#!/bin/python3
# Python Weather Forecast
import datetime as dt
import requests
import json
import simplejson
from typing import List

YR_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
HTTP_DATETIME_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"

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

class Interval:
    """Stores Interval information about weather forecast.
    
    Attributes:
        start_time: Date and time for the start of an interval
        end_time: Date and time for the end of an interval.
        symbol_code: A string representing the coresponding weather icon.
    """
    def __init__(
        self,
        start_time: dt.datetime,
        end_time: dt.datetime,
        symbol_code: str,
    ):
        """Create Interval object
        
        Args:
            start_time: Date and time for the beginning of an interval.
            end_time: Date and time for the end of an interval.
            symbol_code: A string representing the coresponding weather icon.
        """
        self.start_time = start_time
        self.end_time = end_time
        self.symbol_code = symbol_code
    
    @property
    def duration(self) -> dt.timedelta:
        return self.end_time - self.start_time
    

class Data:
    """Class for storing a complete collecion of weather data.
    
    Attributes:
        last_modified: Date and time for when the data was last modified.
        expires: Date and time for when the data expires.
        updated_at: Date and time weather forecast data was updated.
        intervals: A chronological list of data.
        
    Methods:
        intervals_for: Returns the intervals for a specified day.
        intervals_between: Return the intervals for a specified time period.
    """
    
    def __init__(
        self,
        last_modified: dt.datetime,
        expires: dt.datetime,
        updated_at: dt.datetime,
        intervals: List[Interval],
    ):
        """Create an Data object.
        
        Args:
            last_modified: Date and time last modified
            expires: Date and time for when data expires
            updated_at: Date and time the forcast was updated
            intervals: A chronological list of intervals of weather forecacst data.
        """
        self.last_modified = last_modified
        self.expires = expires
        self.updated_at = updated_at
        self.intervals = intervals
        
    def intervals_for(self, day: dt.date) -> List[Interval]:
        """Return interval for given day"""
        relevant_intervals: List[Interval] = []
        
        for interval in self.intervals:
            if interval.start_time.date() == day:
                relevant_intervals.append(interval)
                
        return relevant_intervals
    
    def intervals_between(self, start: dt.datetime, end: dt.datetime) -> List[Interval]:
        """Return intervals between given timeperiod"""
        relevant_intervals: List[Interval] = []
        
        for interval in self.intervals:
            if start <= interval.start_time < end:
                relevant_intervals.append(interval)
                
        return relevant_intervals