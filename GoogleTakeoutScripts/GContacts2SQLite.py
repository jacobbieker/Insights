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
from databaseSetup import Contacts
import csv
from peewee import *
import yaml

with open(os.path.join("..", "constants.yaml"), 'r') as ymlfile:
    constants = yaml.load(ymlfile)

rootdir = os.path.join(constants.get('dataDir'), "Takeout", "Contacts")

with open(os.path.join(rootdir, "All Contacts.csv"), 'r') as source:
    csv_reader = csv.DictReader(x.replace('\0', '') for x in source)
    with open("ContactsOutput.yaml", "a") as output:
        for entry in csv_reader:
            first_name = entry.get("Given Name")
            middle_name = entry.get("Additional Name")
            last_name = entry.get("Family Name")
            alt_name = entry.get("Additional Name")
            birthday = entry.get("Birthday")
            email_1 = entry.get("E-mail 1 - Value")
            email_2 = entry.get("E-mail 2 - Value")
            email_3 = entry.get("E-mail 3 - Value")
            email_4 = entry.get("E-mail 4 - Value")
            nickname = entry.get("Nickname")
            phone_1 = entry.get("Phone 1 - Value")
            phone_2 = entry.get("Phone 2 - Value")
            phone_3 = entry.get("Phone 3 - Value")
            address_1 = entry.get("Address 1 - Formatted")
            #build up query from dictionary parts
            output.write(yaml.dump(entry, default_flow_style=False))
            if first_name is not None:
                if last_name is not None:
                    if middle_name is not None:
                        full_name = first_name + middle_name + last_name
                    else:
                        full_name = first_name + last_name
                else:
                    full_name = first_name
            else:
                full_name = alt_name
            Contacts.insert(name=full_name, birthday=birthday, address=address_1, email_1=email_1, email_2=email_2,
                            email_3=email_3, email_4=email_4, phone_number_1=phone_1, phone_number_2=phone_2,
                            phone_number_3=phone_3).execute()

