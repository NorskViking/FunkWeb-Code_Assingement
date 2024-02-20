#!/bin/python3
# Python Weather Forecast
import datetime as dt
import requests
import json
import simplejson
from typing import Dict, List, Union

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

class Place:
    """Holds data for a place
    
    Attributes:
        name: Name of place
        coordinates: 
    """
    def __init__(
        self,
        name: str,
        latitude: Union[float, int],
        longitude: Union[float, int],
    ):
        """Create Place object
        """
        self.name = name
        self.coordinates: Dict[str, Union[float, int, None]] = {
            "latitude": round(latitude, 4),
            "longitude": round(longitude, 4),
        }

class Variable:
    """Store data of weather variables
    
    """
    def __init__(
        self,
        name: str,
        value: Union[float, int],
        units: str
    ):
        self.name = name
        self.value = value
        self.units = units
        
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Variable):
            return self.value == other.value and self.units == other.units
        if isinstance(other, (int, float)):
            return self.value == other
        return NotImplemented
    
    def __lt__(self, other: object) -> bool:
        if isinstance(other, Variable) and self.units == other.units:
            return self.value < other.value
        if isinstance(other, (int, float)):
            return self.value < other
        return NotImplemented
    
    def __add__(self, other: object) -> "Variable":
        if isinstance(other, Variable) and self.name == other.name and self.units == other.units:
            return Variable(self.name, self.value + other.value, self.units)
        return NotImplemented
    
    def __sub__(self, other: object) -> "Variable":
        if isinstance(other, Variable) and self.name == other.name and self.units == other.units:
            return Variable(self.name, self.value - other.value, self.units)
        return NotImplemented
    

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
        variables: Dict[str, Variable],
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
        self.variables = variables
    
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
    
    
weather_data = requests.get(url, headers=USER_AGENT).json()

#print(first_req)

# Store weather_data in local JSON file.
with open('weather.json', 'w') as json_file:
    json_file.write(simplejson.dumps(weather_data, indent=4))

#response = requests.get(url).json()
#print(response.status_code)

#data = response.text