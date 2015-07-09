__author__ = 'Jacob Bieker'

import json
import os
from datetime import datetime
from peewee import *
import insights
from geopy.geocoders import Nominatim

rootdir = os.path.join(insights.DATA_PATH, "Takeout", "Location")
geolocator = Nominatim()

with open(os.path.join(rootdir, "Location.json"), 'r') as source:
    data = json.dump(source)
    print data