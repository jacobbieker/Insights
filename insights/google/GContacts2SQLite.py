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

from insights.config.databaseSetup import Contacts
from insights.io import config

if __name__ != "__main__":
    configuration_files = config.import_yaml_files(".", ["constants"])
    constants = configuration_files[0]
else:
    configuration_files = config.import_yaml_files("..", ["constants"])
    constants = configuration_files[0]

rootdir = os.path.join(constants.get('dataDir'), "Takeout", "Contacts")

print("Starting Google Contact Parsing")
with open(os.path.join(rootdir, "All Contacts.vcf"), 'rU', encoding='latin-1') as source:
    # Dictionary of values to insert later
    contact_data = []
    num_emails = 0
    num_phones = 0
    for line in source:
        components = line.split(":")
        type_of_data = components[0].split(";")
        if type_of_data[0] == "BEGIN":
            # Start of new record so clear out old data
            print("Begin new contact")
        elif type_of_data[0] == "FN":
            contact_data.append({"name": components[1].replace("\n", "").replace(";", "")})
        elif type_of_data[0] == "EMAIL":
            num_emails += 1
            if(num_emails <= 4):
                dict_name = "email_" + str(num_emails)
                contact_data.append({dict_name: components[1].replace("\n", "").replace(";", "")})
            else:
                print("Too many emails to add")
        elif type_of_data[0] == "TEL":
            num_phones += 1
            if(num_phones <= 4):
                dict_name = "phone_number_" + str(num_phones)
                contact_data.append({dict_name: components[1].replace("\n", "").replace(";", "")})
        elif type_of_data[0] == "item1.ADR":
            contact_data.append({"address": components[1].replace("\n", "").replace(";", "")})
        elif type_of_data[0] == "BDAY":
            contact_data.append({"birthday": components[1].replace("\n", "").replace(";", "")})
        elif type_of_data[0] == "item1.URL":
            contact_data.append({"url": "http:" + str(components[2])})
        elif type_of_data[0] == "END":
            all_contact_data = {}
            for item in contact_data:
                all_contact_data.update(item)
            # Insert Contact into database
            print(all_contact_data)
            Contacts.insert(all_contact_data).execute()
            print("Inserted Contact")
            # Reset data
            del contact_data[:]
            num_phones = 0
            num_emails = 0
