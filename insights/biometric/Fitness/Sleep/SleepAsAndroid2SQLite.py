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
import csv
import os

from insights.config.databaseSetup import Sleep
from insights.io import config

# Have to do this because when the command is called from the import in any subfolder it cannot find the dbconfig
if __name__ != "__main__":
    configuration_files = config.import_yaml_files(".", ["constants"])
    constants = configuration_files[0]
else:
    configuration_files = config.import_yaml_files(".", ["constants"])
    constants = configuration_files[0]

rootdir = os.path.join(constants.get("dataDir"), "Biometric",
                       "Sleep as Android Spreadsheet - Sleep as Android Spreadsheet.csv")


with open(rootdir, 'r') as source:
    reader = csv.DictReader(source)
    other_reader = []
    for row in reader:
        if row['Id'].isdigit():
            other_reader.append(row)
    for i, row in enumerate(other_reader):
        sleep_data = {'start_time': row['From'],
                      'end_time': row['To'],
                      'duration': float(row['Hours'].strip()),
                      'rating': float(row['Rating'].strip()),
                      'comments': row['Comment'],
                      'cycles': int(row['Cycles'].strip()),
                      'deep_sleep': float(row['DeepSleep'].strip()),
                      'noise': float(row['Noise'].strip()),
                      'application': 'Sleep As Android',
                      }
        Sleep.insert(sleep_data).execute()
