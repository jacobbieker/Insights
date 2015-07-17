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
import databaseSetup
from databaseSetup import Contacts, Message, Call, Voicemail
import json
import yaml

with open(os.path.join("..", "constants.yaml"), 'r') as ymlfile:
    constants = yaml.load(ymlfile)

rootdir = os.path.join(constants.get("dataDir"), "Takeout", "Hangouts", "Hangouts.json")

with open(rootdir, "r") as source:
    data = json.load(source)
    conversations = data.get("conversation_state")
    count = 0
    for conversation in conversations:
        #Gets every conversation
        count += 1
        with open("hangouts." + str(count) + ".json", "a") as output:
            json_output = json.dump(conversation, output, sort_keys=True, indent=4)

