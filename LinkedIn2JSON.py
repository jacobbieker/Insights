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
__author__ = 'Jacob'
import csv
import os
import json
import yaml


with open("constants.yaml", 'r') as ymlfile:
    constants = yaml.load(ymlfile)


rootdir = "C:\Users\jacob_000\OneDrive\Personal_Projects\LinkedIn"

for file in os.listdir(rootdir):
    if (file.endswith(".csv")):
        #TODO Use config file for this?
        if(file == "Organizations.csv" or file == "Honors.csv" or file == "Education.csv" or file == "Positions.csv" or
                   file == "Projects.csv" or file == "Courses.csv"):
            with open(os.path.join(rootdir, file), 'r') as source:
                file_name = os.path.splitext(os.path.basename(file))
                csv_reader = csv.DictReader(x.replace('\0', '') for x in source)
                with open(os.path.join(constants.get("outputDir"), 'linkedin.' + file_name[0] + '.json'), 'a') as json_output:
                    for row in csv_reader:
                        json_data = row
                        #Output to file
                        json_array = json.dump(json_data, json_output, sort_keys=True, indent=4)