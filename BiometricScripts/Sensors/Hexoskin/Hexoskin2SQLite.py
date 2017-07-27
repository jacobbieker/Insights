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

import os
import peewee
import requests
import yaml
import sys
import BiometricScripts.Sensors.Hexoskin.HxApi2_0 as hexoskin

#Authentication with Hexoskin
#  Have to do this because when the command is called from the import in any subfolder it cannot find the dbconfig
'''
if __name__ != "__main__":
    with open(os.path.join("access.yaml"), 'r') as access:
        access_config = yaml.load(access)
else:
    with open(os.path.join("access.yaml"), 'r') as access:
        access_config = yaml.load(access)

if __name__ == "__main__":
    with open(os.path.join("constants.yaml"), 'r') as ymlfile:
        constants = yaml.load(ymlfile)
else:
    with open("constants.yaml", 'r') as ymlfile:
        constants = yaml.load(ymlfile)

# Set up auth and data locations
secret = access_config.get('hexoskin')['secret']
client_id = access_config.get('hexoskin')['clientId']

rootdir = os.path.join(constants.get('dataDir'), "Hexoskin")
'''

auth = hexoskin.SessionInfo()

#TODO: List all records, download those that are not already downloaded

records = hexoskin.getRecordList(auth, limit="0")
print(records)

for record_uri in records:
    print(record_uri.get('id'))
    records_request = hexoskin.getRecordData(auth, recordID=record_uri.get('id'), downloadRaw=True)
    print(records_request)