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
import os

from insights.config.databaseSetup import Calendars
from insights.io import config

if __name__ != "__main__":
    configuration_files = config.import_yaml_files(".", ["constants"])
    constants = configuration_files[0]
else:
    configuration_files = config.import_yaml_files("..", ["constants"])
    constants = configuration_files[0]

rootdir = os.path.join(constants.get("dataDir"), "Takeout", "Tasks", "Tasks.json")

print("Starting Google Tasks Parsing")
with open(rootdir, 'r') as source:
    data = json.load(source)
    task_lists = data.get("items")
    for task_list in task_lists:
        print(task_list)
        if task_list.get("items") is not None:
            for todo in task_list.get("items"):
                if todo is not None:
                    task = todo.get("title")
                    updated = todo.get("updated")
                    due = todo.get("due")
                    completed = todo.get("completed")
                    status = todo.get("status")
                    Calendars.insert(is_task=True, name=task, start_date=updated, end_date=completed, type="task",
                                     description=status).execute()
