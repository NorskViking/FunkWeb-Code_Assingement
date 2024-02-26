#!/bin/python3
# Python Weather Forecast
import datetime as dt
import requests
import json
from pathlib import Path
from typing import Dict, List, Union, Optional

YR_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
HTTP_DATETIME_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"

BASE_URL = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?"
USER_AGENT = "Weather_ForeCast jorgen@funkweb.org"

class Place:
    """Holds data for a place
    
    Attributes:
        name: Name of place
        coordinates: latitude and longitude coordinates
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
        self.coordinates: Dict[str, Union[float, int]] = {
            "latitude": round(latitude, 4),
            "longitude": round(longitude, 4),
        }
    
    def __repr__(self) -> str:
        return f"Place({self.name}, {self.coordinates['latitude'], {self.coordinates['longitude']}})"
    
    def __str__(self) -> str:
        return f"{self.name}, lat:{self.coordinates['latitude']} lon:{self.coordinates['longitude']}"

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
        
    def __repr__(self) -> str:
        return f"Variable({self.name}, {self.value}, {self.units})"
    
    def __str__(self) -> str:
        return f"{self.name}: {self.value}{self.units}"
        
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
        
    def __repr__(self) -> str:
        return f"Interval({self.start_time}, {self.end_time}, {self.symbol_code}, {self.variables})"
    
    def __str__(self) -> str:
        string = f"Forecast between {self.start_time} and {self.end_time}:"
        for vaiable in self.variables.values():
            string += f"\n\t{str(vaiable)}"
        return string
        
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Interval):
            return (
                self.start_time == other.start_time
                and self.end_time == other.end_time
                and self.symbol_code == other.symbol_code
                and self.variables == other.variables
            )
    
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
        units: Dict[str, str],
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
        self.units = units
        self.intervals = intervals
        
    def __repr__(self) -> str:
        return (
            f"Data({self.last_modified}, {self.expires}, {self.updated_at}, {self.units},)"
            f"{self.intervals}"
        )
        
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Data):
            return (
                self.last_modified == other.last_modified
                and self.expires == other.expires
                and self.updated_at == other.updated_at
                and self.units == other.units
                and self.intervals == other.intervals
            )
        return NotImplemented
        
    def intervals_for(self, day: dt.date) -> List[Interval]:
        """Return intervals for given day"""
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
    
class Forecast:
    """Retrives, read, store and update weather forecast data.
    
    Attributes:
        place
        user_agent:
        save_location:
        base_url:
        response
        json_string
        json:
        data (dict):
        
    Methods:
        save:
        load:
        update:
    """
    
    def __init__(
        self,
        place: Place,
        user_agent: Optional[str] = None,
        save_location: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        """Create Forecast Object"""
        if not isinstance(place, Place):
            msg = f"{place} is not an available city for the application."
            raise TypeError(msg)
        self.place = place
        
        self.user_agent = user_agent
        self.save_location = "./data"
        self.base_url = base_url
        self.response: requests.Response
        self.json_string: str
        self.json: dict
        self.data: Data

        if user_agent is None:
            self.user_agent = USER_AGENT
        else:
            self.user_agent = user_agent
            
        if base_url is None:
            self.base_url = BASE_URL
        else:
            self.base_url = base_url

        if save_location is None:
            self.save_location = Path("./data").expanduser().resolve()
        else:
            self.save_location = Path(save_location).expanduser().resolve()
    
    @property
    def url(self) -> str:
        
        return f"{self.base_url}"
    
    @property
    def url_parameter(self,) -> Dict[str, Union[int, float]]:
        """Parameters"""
        parameters: Dict[str, Union[int, float]] = {}
        if self.place.coordinates["latitude"] is not None:
            parameters["lat"] = self.place.coordinates["latitude"]
        if self.place.coordinates["longitude"] is not None:
            parameters["lon"] = self.place.coordinates["longitude"]
        
        return parameters
    
    @property
    def url_headers(self) -> Dict[str, str]:
        headers = {
            "User-Agent": self.user_agent,
        }
        if hasattr(self, "data"):
            headers["If-Modified-Since"] = (
                self.data.last_modified.strftime(HTTP_DATETIME_FORMAT) + "GMT"
            )
        
        return headers
    
    @property
    def file_name(self) -> str:
        """File name for the forcast data for a given location"""
        return (
            f"lat{self.place.coordinates["latitude"]}lon{self.place.coordinates["longitude"]}_{self.place.name}.json"
        )
        
    def _json_from_response(self) -> None:
        
        if self.response.status_code == 304:
            self.json["status_code"] = self.response.status_code
            self.json["headers"] = dict(self.response.headers)
            
            self.json_string = json.dumps(self.json)
            
        else:
            json_string = "{"
            json_string += f'"status_code":{self.response.status_code},'
            json_string += f'"headers":{json.dumps(dict(self.response.headers))},'
            json_string += f'"data":{self.response.text}'
            json_string += "}"
            
            self.json_string = json_string
            self.json = json.loads(json_string)
            
    def _parse_json(self) -> None:
        
        json = self.json
        
        last_modified = dt.datetime.strptime(json["headers"]["Last-Modified"], HTTP_DATETIME_FORMAT)
        expires = dt.datetime.strptime(json["headers"]["Expires"], HTTP_DATETIME_FORMAT)
        
        updated_at = dt.datetime.strptime(json["data"]["properties"]["meta"]["updated_at"], YR_DATETIME_FORMAT)
        
        units = json["data"]["properties"]["meta"]["units"]
        
        intervals = []
        
        for timeseries in json["data"]["properties"]["timeseries"]:
            start_time = dt.datetime.strptime(timeseries["time"], YR_DATETIME_FORMAT)
            
            variables = {}
            for var_name, var_value in timeseries["data"]["instant"]["details"].items():
                variables[var_name] = Variable(var_name, var_value, units[var_name])
                
            hours = 0
            if "next_1_hours" in timeseries["data"]:
                hours = 1
            elif "next_6_hours" in timeseries["data"]:
                hours = 6
            elif "next_12_hours" in timeseries["data"]:
                hours = 12
                
            end_time = start_time + dt.timedelta(hours=hours)
            
            if hours != 0:
                symbol_code = timeseries["data"][f"next_{hours}_hours"]["summary"]["symbol_code"]
                
                for var_name, var_value in timeseries["data"][f"next_{hours}_hours"]["details"].items(): 
                    variables[var_name] = Variable(var_name, var_value, units[var_name])
            else:
                symbol_code = None
                
            intervals.append(Interval(start_time, end_time, symbol_code, variables))
            
        self.data = Data(last_modified, expires, updated_at, units, intervals)
        
    def _data_outdated(self) -> bool:
        return self.data.expires < dt.datetime.now()
    
    def save(self) -> None:
        if not self.save_location.exists():
            self.save_location.mkdir(parent=True)
        elif not self.save_location.is_dir():
            raise NotADirectoryError(f"Expected {self.save_location} to be a directory.")
        
        file_path = Path(self.save_location).joinpath(self.file_name)
        file_path.write_text(self.json_string)

    def load(self) -> None:
        file_path = Path(self.save_location).joinpath(self.file_name)
        self.json_string = file_path.read_text()
        self.json = json.loads(self.json_string)
        self._parse_json()
        
    def update(self) -> str:
        
        return_status = ""
        
        if not hasattr(self, "data"):
            file_path = Path(self.save_location).joinpath(self.file_name)
            if file_path.exists():
                self.load()
                
        if hasattr(self, "data") and not self._data_outdated():
            return_status = "Data-Not-Expired"
            return return_status
        
        self.response = requests.get(self.url, params=self.url_parameter, headers=self.url_headers)
        
        if self.response.status_code == 304:
            return_status = "Data-Not-Modified"
        else:
            self.response.raise_for_status()
            return_status = "Data-Modified"
        
        self._json_from_response()
        self.save()
        self._parse_json()
        
        return return_status
    
"""
class City:
    def __init__(
        self
        ):
        self.citys: dict
        
    def get_citys(self) -> None:
        nor_cities = open("./data/nor.json")
        # Convert JSON object to dict
        nor_data = json.load(nor_cities)
        # Close JSON file
        nor_cities.close()
        norwegian_citys = []
        for city in nor_data:
            norwegian_citys.append(Place(city["city"], float(city["lat"]), float(city["lon"])))
        
        self.citys = norwegian_citys
"""        

"""
nor_cities = open("./data/nor.json")
# Convert JSON object to dict
nor_data = json.load(nor_cities)
# Close JSON file
nor_cities.close()
norwegian_citys = []
for city in nor_data:
    norwegian_citys.append(Place(city["city"], float(city["lat"]), float(city["lon"])))

#print(norwegian_citys)

for city in norwegian_citys:
    print(city.name)
    
"""