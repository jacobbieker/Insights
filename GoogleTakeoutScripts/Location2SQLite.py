__author__ = 'Jacob Bieker'

import json
import os
from datetime import datetime
from peewee import *
import setup
from geopy.geocoders import Nominatim

rootdir = os.path.join(setup.DATA_PATH, "Takeout", "Location")
geolocator = Nominatim()

with open(os.path.join(rootdir, "Location.json"), 'r') as source:
    data = json.dump(source)
    print data