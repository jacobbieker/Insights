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
from databaseSetup import Locations
import yaml
import json
from geopy.geocoders import Nominatim, GoogleV3, OpenCage
from geopy.point import Point
from geopy.exc import *

def address_to_parts(address):
    parts = str(address).split(", ")
    return parts

'''
Functions that convert the individual responses into a common format to be put in database
'''
def nominatim_parser(nominatim_response, longitude, latitude):
    '''
    Look at Nomatimin.json as an example

    :param nominatim_response:
    :param longitude:
    :param latitude:
    :return:
    '''
    continent = continent_finder(latitude, longitude)
    provider = "Nominatim"

    return Locations.insert(date=converted_time_stamp,time=time_stamp, longitude=longitude, latitude=latitude,
                            continent=continent, country=country, state=state, zip=zipcode, city=city, street=street,
                            name=building, provider=provider)

def opencage_parser(opencage_response, longitude, latitude):
    '''
    Look at OpenCage.json for an example
    :param opencage_response:
    :return:
    '''
    continent = continent_finder(latitude, longitude)
    provider = "OpenCage"
    return Locations.insert(date=converted_time_stamp,time=time_stamp, longitude=longitude, latitude=latitude,
                            continent=continent, country=country, state=state, zip=zipcode, city=city, street=street,
                            provider=provider)

def googleV3_parser(google_response, longitude, latitude):
    '''
    Looka at Google.json for an example
    :param longitude:
    :param latitude:
    :return:
    '''
    continent = continent_finder(latitude, longitude)
    provider = "Google"
    return Locations.insert(date=converted_time_stamp,time=time_stamp, longitude=longitude, latitude=latitude,
                            continent=continent, country=country, state=state, zip=zipcode, city=city, street=street,
                            name=building, provider=provider)


#Find the continent based off the coordinates, more consistent than going off the name
def continent_finder(latitude, longitude):
    #get the list of country data
    for country_data in location_data.get('countries').get('country'):
        if country_data.get('north') > latitude > country_data.get('south'):
            if country_data.get('east') > longitude > country_data.get('west'):
                return country_data.get('continentName')
    return "Continent Not Found"

with open(os.path.join("..","constants.yaml"), 'r') as ymlfile:
    constants = yaml.load(ymlfile)

#Open continents.yaml to get location data
with open(os.path.join("..", "countries.yaml"), 'r') as loc_data:
    location_data = yaml.load(loc_data)

rootdir = os.path.join(constants.get('dataDir'), "Takeout", "Location History")
opencage_geolocator = OpenCage(api_key="***REMOVED***")
google_geolocator = GoogleV3()
nominatim_geolocator = Nominatim()
locationCache = {}

with open(os.path.join(rootdir, "LocationHistory.json"), 'r') as source:
    data = json.load(source)
    locations = data.get('locations')
    for location in locations:
        print location
        time_stamp = location.get('timestampMs')
        print time_stamp
        converted_time_stamp = datetime.fromtimestamp(float(time_stamp)/1000.0)
        longitude = location.get('longitudeE7')/10000000.0
        latitude = location.get('latitudeE7')/10000000.0
        point_string = str(latitude) + ", " + str(longitude)
        point = Point(latitude=latitude, longitude=longitude)
        #Check if already exist
        if locationCache.has_key(point_string):
            address = locationCache.get(point_string)[0]
            provider = locationCache.get(point_string)[1]
        else:
            try:
                #Try OpenCage first
                time.sleep(2)
                address = opencage_geolocator.reverse(point, exactly_one=True)
                provider = "OpenCage"
                locationCache[point_string] = address.raw, provider
                print address.raw
                opencage_parser(address.raw, longitude, latitude).execute()
            except GeocoderQuotaExceeded or GeocoderTimedOut:
                try:
                    #Try GoogleV3 next
                    time.sleep(3)
                    address = google_geolocator.reverse(point, exactly_one=True)
                    provider = "Google"
                    locationCache[point_string] = address.raw, provider
                    print address.raw
                    googleV3_parser(address.raw, longitude, latitude)
                except GeocoderQuotaExceeded or GeocoderTimedOut:
                    try:
                        #Try Nominatum last
                        #To not overload OSM servers, they request a delay of atleast 1 second per request, add some extra
                        time.sleep(5)
                        address = nominatim_geolocator.reverse(point, exactly_one=True)
                        provider = "Nominatim"
                        locationCache[point_string] = address.raw, provider
                        print address.raw
                        nominatim_parser(address.raw, longitude, latitude).execute()
                    except GeocoderQuotaExceeded or GeocoderTimedOut:
                        print "Could not access geocoders for location: " + point_string
                        exit() #Exits if it cannot get all the location data