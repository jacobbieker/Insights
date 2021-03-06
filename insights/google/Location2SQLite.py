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

import os
import time
from datetime import datetime
from insights.config.databaseSetup import Locations
from insights.config import databaseSetup
from peewee import DoesNotExist
import yaml
import json
from geopy.geocoders import Nominatim, GoogleV3, OpenCage, Bing, GeoNames
from geopy.point import Point
from geopy.exc import *

'''
Variables used by multiple functions
'''


# List holding the values to be bulk inserted
location_bulk_insert_queries = []
# Changing the nmber below affects how often inserts are made, as well as location in data saved
number_entries_before_action = 10
# default, so that current_location_saver will work with google_location_parse
number_entries_searched = number_entries_before_action * 2

# Dictionary to hold the tuple of longitude and latitude so do not have to touch the database unless necessary
location_dict = {}

print("Starting Location Parsing")


def address_to_parts(address):
    parts = str(address).split(", ")
    return parts


def location_to_dict(longitude_query, latitude_query, type, response):
    location_dict[(longitude_query, latitude_query, type)] = response


'''
Remove elements from the Locations JSON as it is consumed, overwriting a file as it goes, which is then loaded, if it
 exists at the next run of the script
'''


def current_position_saver(keys):
    '''
    Save the current position after every X insertions
    '''
    # temp_list = dictionary
    # del temp_list[0:keys] # Delete the keys from first to whatever key it is
    with open(os.path.join(constants.get("outputDir"), "LocationsIndex"), "w") as temp_file:
        print("Dumping " + str(keys) + " Records")
        if keys < number_entries_before_action:
            temp_file.write(yaml.dump(str(keys)))
        else:
            # Just to make sure that none are skipped, wirtes a number lower than the actual, not too much performance
            # impact, relative to going through them all again, for bigger performance gain, delete the negative
            temp_file.write(yaml.dump(str(keys - number_entries_before_action)))


def can_load_last_position():
    if os.path.isfile(os.path.join(constants.get("outputDir"), "LocationsIndex")):
        return True
    else:
        return False


def insert_many_locations(locations_list):
    """
    Executes multiple inserts at once, to reduce amount of time the database is locked
    :param locations_list:
    :return:
    """
    if len(locations_list) >= number_entries_before_action:
        # with databaseSetup.database.atomic():  WOULD INCREASE SPEED, IMPORT PROBLEMS
        Locations.insert_many(locations_list).execute()
        print("Inserted " + str(len(locations_list)) + " Records")
        del locations_list[:]


'''
Query database if it exists, and try to retrive a record for the current lat and long in the request
'''


def get_locations_from_database(longitude_query, latitude_query):
    """
    Go through database and check if the location was already queried
    :rtype : bool
    :param longitude_query:
    :param latitude_query:
    :return: Whether query already exists in database
    """

    # Currently doesn't work in that once the database is large enough, peewee times out on the SQL search, stopping the
    # program
    return False
    '''
    try:
        # Try to location and getting same time, reduce duplicates
        loc_model = Locations.get(((Locations.latitude == latitude_query) & (Locations.longitude == longitude_query)) &
                                  (Locations.time == time_stamp))
        return True
    except DoesNotExist:
        try:
            loc_model = Locations.get((
                (Locations.bound_north >= latitude_query >= Locations.bound_south) &
                (Locations.bound_east >= longitude_query >= Locations.bound_west)))

            # Recomment out if removing larger comment
                Locations.insert({'date': converted_time_stamp, 'time': time_stamp, 'longitude': longitude_query,
                                  'latitude': latitude_query,
                                  'continent': loc_model.continent, 'country': loc_model.country, 'state': loc_model.state,
                                  'zip': loc_model.zip, 'area': loc_model.area, 'county': loc_model.county,
                                  'city': loc_model.city, 'street': loc_model.street, 'name': loc_model.name,
                                  'provider': loc_model.provider, 'bound_north': loc_model.bound_north,
                                  'bound_east': loc_model.bound_east, 'bound_south': loc_model.bound_south,
                                  'bound_west': loc_model.bound_west})
            # Recomment out
            location_bulk_insert_queries.append(
                {'date': converted_time_stamp, 'time': time_stamp, 'longitude': longitude_query,
                 'latitude': latitude_query,
                 'continent': loc_model.continent, 'country': loc_model.country, 'state': loc_model.state,
                 'zip': loc_model.zip, 'area': loc_model.area, 'county': loc_model.county,
                 'city': loc_model.city, 'street': loc_model.street, 'name': loc_model.name,
                 'provider': loc_model.provider, 'bound_north': loc_model.bound_north,
                 'bound_east': loc_model.bound_east, 'bound_south': loc_model.bound_south,
                 'bound_west': loc_model.bound_west})
            location_to_dict(longitude_query=longitude_query, latitude_query=latitude_query, type="Database",
                             response={'date': converted_time_stamp, 'time': time_stamp, 'longitude': longitude_query,
                              'latitude': latitude_query,
                              'continent': loc_model.continent, 'country': loc_model.country, 'state': loc_model.state,
                              'zip': loc_model.zip, 'area': loc_model.area, 'county': loc_model.county,
                              'city': loc_model.city, 'street': loc_model.street, 'name': loc_model.name,
                              'provider': loc_model.provider, 'bound_north': loc_model.bound_north,
                              'bound_east': loc_model.bound_east, 'bound_south': loc_model.bound_south,
                              'bound_west': loc_model.bound_west})
            insert_many_locations(location_bulk_insert_queries)
            return True
        except DoesNotExist:
            print("Error: Does not Exist")
            return False
    '''


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
    nominatim_data = nominatim_response.get("address")
    building = nominatim_data.get("building")
    city = nominatim_data.get("city")
    country = nominatim_data.get("country")
    county = nominatim_data.get("county")
    street = nominatim_data.get("pedestrian")
    zipcode = nominatim_data.get("postcode")
    state = nominatim_data.get("state")
    area = nominatim_data.get("suburb")
    continent = continent_finder(latitude, longitude)
    provider_type = "Nominatim"
    northeast = [latitude, longitude]
    southwest = [latitude, longitude]
    location_to_dict(longitude_query=longitude, latitude_query=latitude, response=nominatim_response, type="Nominatim")

    return [Locations.insert(date=converted_time_stamp, time=time_stamp, longitude=longitude, latitude=latitude,
                             continent=continent, country=country, state=state, zip=zipcode, area=area, county=county,
                             city=city, street=street, name=building, provider=provider_type, bound_north=northeast[0],
                             bound_east=northeast[1], bound_south=southwest[0], bound_west=southwest[1]), northeast,
            southwest, {"date": converted_time_stamp, "time": time_stamp, "longitude": longitude, "latitude": latitude,
                        "continent": continent, "country": country, "state": state, "zip": zipcode, "area": area,
                        "county": county, "city": city, "street": street, "name": building, "provider": provider_type,
                        "bound_north": northeast[0], "bound_east": northeast[1], "bound_south": southwest[0],
                        "bound_west": southwest[1]}]


def opencage_parser(opencage_response, longitude, latitude):
    '''
    Look at OpenCage.json for an example
    :param opencage_response:
    :return:
    '''
    opencage_data = opencage_response.get("components")
    building = opencage_data.get("house")
    if building is None:
        building = opencage_data.get("building")
        if building is None:
            building = opencage_data.get("house_number")
    city = opencage_data.get("city")
    country = opencage_data.get("country")
    county = opencage_data.get("county")
    street = opencage_data.get("road")
    if street is None:
        street = opencage_data.get("pedestrian")
    zipcode = opencage_data.get("postcode")
    state = opencage_data.get("state")
    area = opencage_data.get("suburb")
    continent = continent_finder(latitude, longitude)
    provider_type = "OpenCage"
    bounds = opencage_response.get("bounds")
    northeast = [bounds.get("northeast").get("lat"), bounds.get("northeast").get("lng")]
    southwest = [bounds.get("southwest").get("lat"), bounds.get("southwest").get("lng")]
    location_to_dict(longitude_query=longitude, latitude_query=latitude, response=opencage_response, type="OpenCage")

    return [Locations.insert(date=converted_time_stamp, time=time_stamp, longitude=longitude, latitude=latitude,
                             continent=continent, country=country, state=state, zip=zipcode, area=area, county=county,
                             city=city, street=street, name=building, provider=provider_type, bound_north=northeast[0],
                             bound_east=northeast[1], bound_south=southwest[0], bound_west=southwest[1]), northeast,
            southwest, {"date": converted_time_stamp, "time": time_stamp, "longitude": longitude, "latitude": latitude,
                        "continent": continent, "country": country, "state": state, "zip": zipcode, "area": area,
                        "county": county, "city": city, "street": street, "name": building, "provider": provider_type,
                        "bound_north": northeast[0], "bound_east": northeast[1], "bound_south": southwest[0],
                        "bound_west": southwest[1]}]


def googleV3_parser(google_response, longitude, latitude):
    '''
    Look at Google.json for an example
    :param longitude:
    :param latitude:
    :return:
    '''
    google_data = google_response.get("address_components")
    street = ""
    area = ""
    city = ""
    county = ""
    country = ""
    state = ""
    zipcode = ""
    building = ""
    for piece in google_data:
        type_of_data = piece.get("types")[0]
        name = piece.get("long_name")
        if type_of_data == "route":
            street = name
        elif type_of_data == "neighborhood":
            area = name
        elif type_of_data == "locality":
            city = name
        elif type_of_data == "administrative_area_level_2":
            county = name
        elif type_of_data == "administrative_area_level_1":
            state = name
        elif type_of_data == "country":
            country = name
        elif type_of_data == "postal_code":
            zipcode = name
        elif type_of_data == "street_number":
            building = name
    continent = continent_finder(latitude, longitude)
    provider_type = "Google"
    bounds = google_response.get("geometry").get("viewport")
    northeast = [bounds.get("northeast").get("lat"), bounds.get("northeast").get("lng")]
    southwest = [bounds.get("southwest").get("lat"), bounds.get("southwest").get("lng")]
    location_to_dict(longitude_query=longitude, latitude_query=latitude, response=google_response, type="Google")

    return [Locations.insert(date=converted_time_stamp, time=time_stamp, longitude=longitude, latitude=latitude,
                             continent=continent, country=country, state=state, zip=zipcode, area=area, county=county,
                             city=city, street=street, name=building, provider=provider_type, bound_north=northeast[0],
                             bound_east=northeast[1], bound_south=southwest[0], bound_west=southwest[1]), northeast,
            southwest, {"date": converted_time_stamp, "time": time_stamp, "longitude": longitude, "latitude": latitude,
                        "continent": continent, "country": country, "state": state, "zip": zipcode, "area": area,
                        "county": county, "city": city, "street": street, "name": building, "provider": provider_type,
                        "bound_north": northeast[0], "bound_east": northeast[1], "bound_south": southwest[0],
                        "bound_west": southwest[1]}]


# Find the continent based off the coordinates, more consistent than going off the name
def continent_finder(latitude, longitude):
    """
    Returns the continent that that latitude and longitute correspond to
    :param latitude: Latitude
    :param longitude: Longitude
    :return: Continent that contains those coordinates
    """
    # get the list of country data
    for country_data in location_data.get('countries').get('country'):
        if country_data.get('north') >= latitude >= country_data.get('south'):
            if country_data.get('east') >= longitude >= country_data.get('west'):
                return country_data.get('continentName')
    return "Continent Not Found"


def track_bounds(northeast, southwest, latitude, longitude):
    """
    Keeps track of bounds of geocoding, so that less requests are sent to remote servers
    :param northeast: Northeast coordinates tuple (North, East)
    :param southwest: Southwest Coordinates tuple (South, West)
    :param latitude: Lat of point
    :param longitude: Long of point
    :return: If the lat and long is within the bounds
    """
    northern_most = northeast[0]
    eastern_most = northeast[1]
    southern_most = southwest[0]
    western_most = southwest[1]
    return (northern_most >= latitude >= southern_most) and (eastern_most >= longitude >= western_most)


def location_from_dict(longitude_query, latitude_query, type_query):
    """
    Tries to get response from dictionary and inserts into database if necessary
    :param longitude_query:
    :param latitude_query:
    :param type_query:
    :return:
    """
    try:
        location = location_dict.get((longitude_query, latitude_query, type_query))
        if location:
            if type_query == "Google":
                loc_model = googleV3_parser(location, longitude=longitude_query, latitude=latitude_query)[3]
                location_bulk_insert_queries.append(
                    {'date': converted_time_stamp, 'time': time_stamp, 'longitude': longitude_query,
                     'latitude': latitude_query,
                     'continent': loc_model.get('continent'), 'country': loc_model.get('country'),
                     'state': loc_model.get('state'),
                     'zip': loc_model.get('zip'), 'area': loc_model.get('area'), 'county': loc_model.get('county'),
                     'city': loc_model.get('city'), 'street': loc_model.get('street'), 'name': loc_model.get('name'),
                     'provider': loc_model.get('provider'), 'bound_north': loc_model.get('bound_north'),
                     'bound_east': loc_model.get('bound_east'), 'bound_south': loc_model.get('bound_south'),
                     'bound_west': loc_model.get('bound_west')})
                insert_many_locations(location_bulk_insert_queries)
            elif type_query == "Nominatim":
                loc_model = nominatim_parser(location, longitude=longitude_query, latitude=latitude_query)[3]
                location_bulk_insert_queries.append(
                    {'date': converted_time_stamp, 'time': time_stamp, 'longitude': longitude_query,
                     'latitude': latitude_query,
                     'continent': loc_model.get('continent'), 'country': loc_model.get('country'),
                     'state': loc_model.get('state'),
                     'zip': loc_model.get('zip'), 'area': loc_model.get('area'), 'county': loc_model.get('county'),
                     'city': loc_model.get('city'), 'street': loc_model.get('street'), 'name': loc_model.get('name'),
                     'provider': loc_model.get('provider'), 'bound_north': loc_model.get('bound_north'),
                     'bound_east': loc_model.get('bound_east'), 'bound_south': loc_model.get('bound_south'),
                     'bound_west': loc_model.get('bound_west')})
                insert_many_locations(location_bulk_insert_queries)
            elif type_query == "OpenCage":
                loc_model = opencage_parser(location, longitude=longitude_query, latitude=latitude_query)[3]
                location_bulk_insert_queries.append(
                    {'date': converted_time_stamp, 'time': time_stamp, 'longitude': longitude_query,
                     'latitude': latitude_query,
                     'continent': loc_model.get('continent'), 'country': loc_model.get('country'),
                     'state': loc_model.get('state'),
                     'zip': loc_model.get('zip'), 'area': loc_model.get('area'), 'county': loc_model.get('county'),
                     'city': loc_model.get('city'), 'street': loc_model.get('street'), 'name': loc_model.get('name'),
                     'provider': loc_model.get('provider'), 'bound_north': loc_model.get('bound_north'),
                     'bound_east': loc_model.get('bound_east'), 'bound_south': loc_model.get('bound_south'),
                     'bound_west': loc_model.get('bound_west')})
                insert_many_locations(location_bulk_insert_queries)
            elif type_query == "Database":
                location_bulk_insert_queries.append(response)
                insert_many_locations(location_bulk_insert_queries)
            print("Found match in Dictionary")
            return True
        else:
            return False
    except KeyError:
        print("Key Error: Not found in Dictionary")
        return False


from insights.io import config

if __name__ != "__main__":
    configuration_files = config.import_yaml_files(".", ["constants", "keys", "countries.yaml"])
    constants = configuration_files[0]
    key_file = configuration_files[1]
    location_data = configuration_files[2]
else:
    configuration_files = config.import_yaml_files("..", ["constants", "keys", "countries.yaml"])
    constants = configuration_files[0]
    key_file = configuration_files[1]
    location_data = configuration_files[2]

rootdir = os.path.join(constants.get('dataDir'), "Takeout", "Location History")
opencage_geolocator = OpenCage(api_key=str(key_file.get('opencage').get('key')))
google_geolocator = GoogleV3()
nominatim_geolocator = Nominatim()

if can_load_last_position():
    with open(os.path.join(constants.get("outputDir"), "LocationsIndex"), "r") as checkpoint:
        start_pos_data = yaml.load(checkpoint)
        print(int(start_pos_data))
        with open(os.path.join(rootdir, "Location History.json"), 'r') as source:
            data = json.load(source)
        locations = data.get('locations')
        for key, location in enumerate(locations):
            if key < int(start_pos_data):
                print("Skipping Key " + str(key))
                continue
            time_stamp = location.get('timestampMs')
            converted_time_stamp = datetime.fromtimestamp(float(time_stamp) / 1000.0)
            longitude = location.get('longitudeE7') / 10000000.0
            latitude = location.get('latitudeE7') / 10000000.0
            point_string = str(latitude) + ", " + str(longitude)
            point = Point(latitude=latitude, longitude=longitude)
            if (key % number_entries_before_action) == 0:
                current_position_saver(key)
            if location_from_dict(longitude_query=longitude, latitude_query=latitude, type_query="Google"):
                continue
            elif location_from_dict(longitude_query=longitude, latitude_query=latitude, type_query="Nominatim"):
                continue
            elif location_from_dict(longitude_query=longitude, latitude_query=latitude, type_query="OpenCage"):
                continue
            elif get_locations_from_database(longitude_query=longitude, latitude_query=latitude):
                continue
            else:
                # noinspection PyBroadException
                try:
                    print("Google")
                    # Try GoogleV3 next
                    time.sleep(2)
                    address = google_geolocator.reverse(point, exactly_one=True)
                    provider = "Google"
                    with open("GoogleV3.json", "a") as output:
                        json.dump(address.raw, output, sort_keys=True, indent=4)
                        output.write(",\n")
                    response = googleV3_parser(address.raw, longitude, latitude)
                    response[0].execute()
                except:
                    # noinspection PyBroadException
                    try:
                        print("Open Street Map")
                        # Try Nominatum last
                        # To not overload OSM servers, they request a delay of atleast 1 second per request, add some extra
                        time.sleep(2)
                        address = nominatim_geolocator.reverse(point, exactly_one=True)
                        provider = "Nominatim"
                        with open("Nominatim.json", "a") as output:
                            json.dump(address.raw, output, sort_keys=True, indent=4)
                            output.write(",\n")
                        response = nominatim_parser(address.raw, longitude, latitude)
                        response[0].execute()
                    except:
                        try:
                            print("OpenCage")
                            # Try OpenCage first
                            time.sleep(2)
                            address = opencage_geolocator.reverse(point, exactly_one=True)
                            provider = "OpenCage"
                            with open("OpenCage.json", "a") as output:
                                json.dump(address.raw, output, sort_keys=True, indent=4)
                                output.write(",\n")
                            response = opencage_parser(address.raw, longitude, latitude)
                            response[0].execute()
                        except GeocoderQuotaExceeded or GeocoderTimedOut or GeocoderServiceError:
                            print("Could not access geocoders for location: " + point_string)
                            break  # Skips if cannot find locat
        if len(location_bulk_insert_queries) != 0:
            Locations.insert_many(location_bulk_insert_queries).execute()
            print("Inserted " + str(len(location_bulk_insert_queries)) + " Records")
else:
    with open(os.path.join(rootdir, "Location History.json"), 'r') as source:
        data = json.load(source)
        locations = data.get('locations')
        for key, location in enumerate(locations):
            time_stamp = location.get('timestampMs')
            converted_time_stamp = datetime.fromtimestamp(float(time_stamp) / 1000.0)
            longitude = location.get('longitudeE7') / 10000000.0
            latitude = location.get('latitudeE7') / 10000000.0
            point_string = str(latitude) + ", " + str(longitude)
            point = Point(latitude=latitude, longitude=longitude)
            if (key % number_entries_before_action) == 0:
                current_position_saver(key)
            if location_from_dict(longitude_query=longitude, latitude_query=latitude, type_query="Google"):
                continue
            elif location_from_dict(longitude_query=longitude, latitude_query=latitude, type_query="Nominatim"):
                continue
            elif location_from_dict(longitude_query=longitude, latitude_query=latitude, type_query="OpenCage"):
                continue
            elif get_locations_from_database(longitude_query=longitude, latitude_query=latitude):
                continue
            else:
                # noinspection PyBroadException
                try:
                    # Try GoogleV3 next
                    print("Google")
                    time.sleep(2)
                    address = google_geolocator.reverse(point, exactly_one=True)
                    provider = "Google"
                    with open("GoogleV3.json", "a") as output:
                        json.dump(address.raw, output, sort_keys=True, indent=4)
                        output.write(",\n")
                    response = googleV3_parser(address.raw, longitude, latitude)
                    response[0].execute()
                except:
                    # noinspection PyBroadException
                    try:
                        # Try Nominatum last
                        # To not overload OSM servers, they request a delay of atleast 1 second per request, add some extra
                        print("Open Street Map")
                        time.sleep(2)
                        address = nominatim_geolocator.reverse(point, exactly_one=True)
                        provider = "Nominatim"
                        with open("Nominatim.json", "a") as output:
                            json.dump(address.raw, output, sort_keys=True, indent=4)
                            output.write(",\n")
                        response = nominatim_parser(address.raw, longitude, latitude)
                        response[0].execute()
                    except:
                        try:
                            # Try OpenCage first
                            print("OpenCage")
                            time.sleep(2)
                            address = opencage_geolocator.reverse(point, exactly_one=True)
                            provider = "OpenCage"
                            with open("OpenCage.json", "a") as output:
                                json.dump(address.raw, output, sort_keys=True, indent=4)
                                output.write(",\n")
                            response = opencage_parser(address.raw, longitude, latitude)
                            response[0].execute()
                        except GeocoderQuotaExceeded or GeocoderTimedOut or GeocoderServiceError:
                            print("Could not access geocoders for location: " + point_string)
                            break  # Skips if cannot find locat
        if len(location_bulk_insert_queries) != 0:
            Locations.insert_many(location_bulk_insert_queries).execute()
            print("Inserted " + str(len(location_bulk_insert_queries)) + " Records")
