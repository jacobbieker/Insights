'''
Copyright (C) 2015  Jacob Bieker, jacob@bieker.us, www.jacobbieker.com

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
'''
__author__ = 'Jacob Bieker'

import json
import os
import time
from datetime import datetime
from peewee import *
from databaseSetup import Locations
import yaml
from geopy.geocoders import Nominatim

def address_to_parts(address):
    parts = str(address).split(", ")
    print parts

with open(os.path.join("..","constants.yaml"), 'r') as ymlfile:
    constants = yaml.load(ymlfile)

rootdir = os.path.join(constants.get('dataDir'), "Takeout", "Location History")
geolocator = Nominatim()
locationCache = {}

with open(os.path.join(rootdir, "LocationHistory.json"), 'r') as source:
    data = json.load(source)
    locations = data.get('locations')
    for location in locations:
        time_stamp = location.get('timestampMS')
        longitude = location.get('longitudeE7')/10000000.0
        latitude = location.get('latitudeE7')/10000000.0
        point = str(latitude) + ", " + str(longitude)
        if locationCache.has_key(point):
            address = locationCache.get(point)
        else:
            #To not overload OSM servers, they request a delay of atleast 1 second per request, add some extra
            time.sleep(5)
            address = geolocator.reverse(point)
            locationCache[point] = address
        print address
        parts = address_to_parts(address)
        #Break up return into parts
        amount = len(parts)
        country = parts[amount - 1]
        zipcode = parts[amount - 2]
        state = parts[amount - 3]
        county = parts[amount - 4]
        city = parts[amount - 5]
        area = parts[amount - 6]
        street = parts[amount -7]
        if amount > 8:
            number = parts[amount - 8]
            building = parts[amount - 9]
        else:
            building = parts[amount - 8]
            number = ""

        #Based off own data, two options
        if country == "United States of America" or "Canada" or "Mexico":
            continent = "North America"
        else:
            continent = "Europe"

        Locations.insert(time=time_stamp, longitude=longitude, latitude=latitude).execute()

    #TODO GO through each json object below locations, taking timestampMS, latitudeE7, longitudeE7
