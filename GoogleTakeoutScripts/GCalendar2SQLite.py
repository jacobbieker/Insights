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
import yaml
from glob import glob
from databaseSetup import Calendars

with open(os.path.join("..", "constants.yaml"), 'r') as ymlfile:
    constants = yaml.load(ymlfile)

rootdir = os.path.join(constants.get("dataDir"), "Takeout", "Calendar")
calendars = [y for x in os.walk(rootdir) for y in glob(os.path.join(x[0], '*.ics'))]

for calendar in calendars:
    with open(calendar, "r", encoding="latin-1") as source:
        # Dictionary of values to insert later
        event_data = []
        which_calendar = os.path.basename(calendar)
        which_calendar = which_calendar.replace(".ics", "")
        print(which_calendar)
        for line in source:
            components_temp = line.split(":")
            components = []
            for component in components_temp:
                component = component.replace("\n", "")
                components.append(component)
            type_of_data = components[0].split(";")
            if type_of_data[0] == "BEGIN" and components[1] == "VEVENT":
                event_data.append({"which_calendar": which_calendar})
                event_data.append({"is_task": False})
                # Start of new record
                print("Begin new event")
            elif type_of_data[0] == "DTSTART":
                #TODO Split into start date and start time
                event_data.append({"start_time": components[1]})
            elif type_of_data[0] == "DTEND":
                event_data.append({"end_time": components[1]})
            elif type_of_data[0] == "DESCRIPTION":
                event_data.append({"description": components[1]})
            elif type_of_data[0] == "LOCATION":
                event_data.append({"location": components[1]})
            elif type_of_data[0] == "SUMMARY":
                event_data.append({"name": components[1]})
            elif type_of_data[0] == "END" and components[1] == "VEVENT":
                all_event_data = {}
                for item in event_data:
                    all_event_data.update(item)
                # Insert Contact into database
                print(all_event_data)
                Calendars.insert(all_event_data).execute()
                print("Inserted Event")
                # Reset data
                del event_data[:]
