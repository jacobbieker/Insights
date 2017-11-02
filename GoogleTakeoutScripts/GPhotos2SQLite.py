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
import yaml
import os
from databaseSetup import Photos
from glob import glob
import exifread
from io import config

if __name__ != "__main__":
    configuration_files = config.import_yaml_files(".", ["constants"])
    constants = configuration_files[0]
else:
    configuration_files = config.import_yaml_files("..", ["constants"])
    constants = configuration_files[0]

rootdir = os.path.join(constants.get("dataDir"), "Takeout", "Google Photos")
photo_data = [y for x in os.walk(rootdir) for y in glob(os.path.join(x[0], '*.json'))]

print("Starting Google Photo Parsing")
for json_file in photo_data:
    with open(json_file, 'r') as file:
        metadata = json.dump(file)
