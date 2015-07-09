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
from datetime import datetime
from peewee import *
import insights
from geopy.geocoders import Nominatim

rootdir = os.path.join(insights.DATA_PATH, "Takeout", "Location")
geolocator = Nominatim()

with open(os.path.join(rootdir, "LocationHistory.json"), 'r') as source:
    data = json.dump(source)
    #TODO GO through each json object below locations, taking timestampMS, latitudeE7, longitudeE7
