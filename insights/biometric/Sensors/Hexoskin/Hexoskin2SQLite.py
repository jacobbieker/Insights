__author__ = 'jacob'
'''
Copyright (C) 2017  Jacob Bieker, jacob@bieker.us, www.jacobbieker.com

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

import json
import os
from pathlib import Path
from pprint import pprint

from playhouse.dataset import DataSet

import insights.biometric.Sensors.Hexoskin.HxApi2_0 as hexoskin
from insights.io import config

#Authentication with Hexoskin
#  Have to do this because when the command is called from the import in any subfolder it cannot find the dbconfig

if __name__ != "__main__":
    configuration_files = config.import_yaml_files(".", ["access.yaml", "keys", "constants"])
    access_config = configuration_files[0]
    hexoskin_access = configuration_files[1]
    constants = configuration_files[2]

else:
    configuration_files = config.import_yaml_files(os.path.join("..", "..", ".."), ["access.yaml", "keys", "constants"])
    access_config = configuration_files[0]
    hexoskin_access = configuration_files[1]
    constants = configuration_files[2]

# Open connection to database with Dataset, probably future way of connecting to database for this, easy import of
# JSON data
database = DataSet("sqlite:///"+constants.get("databaseLoc"))
# Set up auth and data locations
secret = access_config.get('hexoskin')['secret']
client_id = access_config.get('hexoskin')['clientId']

rootdir = os.path.join(constants.get('dataDir'), "Hexoskin")


auth = hexoskin.SessionInfo(publicKey=str(hexoskin_access.get('hexoskin').get('clientId')),
                            privateKey=str(hexoskin_access.get('hexoskin').get('secret')),
                            username=str(hexoskin_access.get('hexoskin').get('email')),
                            password=str(hexoskin_access.get('hexoskin').get('password')))

#TODO: List all records, download those that are not already downloaded

records = hexoskin.getRecordList(auth, limit="0")
#print(records)

downloaded_ones = []
for index, thing in enumerate(os.walk(rootdir)):
    if index == 0:
        downloaded_ones = thing[1]

print("___________________ Downloaded Hexoskin Records:")
print(downloaded_ones)

for record_uri in records:
    print(record_uri.get('id'))
    if str(record_uri.get('id')) not in downloaded_ones:
        #print(record_uri.get('id'))
        records_request = hexoskin.getRecordData(auth, recordID=record_uri.get('id'), downloadProcessed=True)
        pprint(records_request.keys())
        path = Path(os.path.join(rootdir, str(record_uri.get('id'))+".txt"))
        pprint(records_request['info'], open(path, "w+"))
        path = Path(os.path.join(rootdir, str(record_uri.get('id'))+"_print.txt"))
        output_file = open(path, "w+")
        pprint(records_request['annotations'], output_file)
        print(isinstance(records_request, dict))
        for key, value in records_request.items():
            if value:
                path = Path(os.path.join(rootdir, str(record_uri.get('id')), str(record_uri.get('id')) + "_" + str(key)))
                path.parent.mkdir(parents=True, exist_ok=True)
                #print(value)
                try:
                    with open(path, "w+") as fp:
                        json.dump(value, fp=fp, indent=4)
                except TypeError as e:
                    print("Type Error, need to fix: ")
                    print(value)
                    print(str(e))
                    continue
    else:
        print("Skipping: " + str(record_uri.get('id')))
