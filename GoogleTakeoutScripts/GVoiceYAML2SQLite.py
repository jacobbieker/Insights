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
from peewee import *
from databaseSetup import Message, Contacts, Voicemail, Call
import os
import yaml
from glob import glob

def voicemail2SQLite(voicemail):
    caller = voicemail.get("caller")
    duration = voicemail.get("duration")
    time = voicemail.get("time")
    number = voicemail.get("phone number")
    message = voicemail.get("message")
    Voicemail.insert(date=time, caller=caller, message=message)

def text2SQLite(text):
    sender = text.get("sender")
    reciever = text.get("reciever")
    time = text.get("time")
    number = text.get("number")
    message = text.get("message")

def call2SQLite(call):
    caller = call.get("caller")
    status = call.get("status")
    time = call.get("time")
    duration = call.get("duration")
    number = call.get("phone number")


with open(os.path.join("..", "constants.yaml"), 'r') as ymlfile:
    constants = yaml.load(ymlfile)

location = constants.get("outputDir")
#Walk through and get every gvoice. file in output directory
conversations = [y for x in os.walk(location) for y in glob(os.path.join(x[0], 'gvoice.*'))]

for conversation in conversations:
    #Go through each file
    messages = yaml.load(conversations)
    for message in messages:
        #Each individual message now
        type = message.get("type")
        if type == "sms":
            text2SQLite(message)
        elif type == "voicemail":
            voicemail2SQLite(message)
        elif type == "call":
            call2SQLite(message)
