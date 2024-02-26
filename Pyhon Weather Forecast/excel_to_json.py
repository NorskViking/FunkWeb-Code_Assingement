#!/bin/Python3
import json
import simplejson
import pandas

"""
    The purpose of this program is to read an excel file downloaded from simplemaps.com and convert
    it into a JSON file, for use in my weather app. 
    
    Using the free version Excel file downloaded from https://simplemaps.com/data/world-cities
    wich gives City name, and longitude and latitude informtion from 43.000 cities around the world.
"""

# Read excel files and store only columns with the data we want to use, ignore unneeded data columns
excel_data_df = pandas.read_excel("./data/worldcities.xlsx", usecols=['city', 'lat', 'lon', 'country'], converters={'city':str,'lat':str,'lon':str,'country':str})
# Convert to JSON
json_str = excel_data_df.to_json(orient='records')
# Load into JSON dict
json_dict = json.loads(json_str)

# Create empty dict for storing only Norwegian cities
norway_dict = []
# Loop thru the full dict and append Norwegian cities into norway_dict
for city in json_dict:
    if city['country'] == 'Norway':
        norway_dict.append(city)

# Write all Norwegian cities from Excel file, into its own json file, with indent of 4 for easier reading
with open('./data/nor.json', 'w') as json_file:
    json_file.write(simplejson.dumps(norway_dict, indent=4))

# Write all Cities from Excel file into json file, with indent of 4 for easier reading
with open('./data/city_data.json', 'w') as json_file:
    json_file.write(simplejson.dumps(json_dict, indent=4))
