__author__ = 'Jacob Bieker'

import json
import os
from datetime import datetime
from peewee import *
import setup

rootdir = os.path.join(setup.DATA_PATH, "Takeout", "Location")

