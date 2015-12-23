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
import datetime

def get_particpant(participant):
    name = participant.get("fallback_name")
    chat_id = participant.get("id").get("chat_id")
    phone_data = participant.get("phone_number")
    number = phone_data.get("e164")
    international_number = phone_data.get("i18n_data").get("international_number")
    national_number = phone_data.get("i18n_data").get("national_number")
    if databaseSetup.get_contact_by_number(number) is None:
        if databaseSetup.get_contact_by_number(international_number) is None:
            if databaseSetup.get_contact_by_number(national_number) is None:
                if Contacts.get(name=name):
                    contact = Contacts.get(name=name)
                else:
                    contact = None
                contact = None
            else:
                contact = databaseSetup.get_contact_by_number(national_number)
        else:
            contact = databaseSetup.get_contact_by_number(international_number)
    else:
        contact = databaseSetup.get_contact_by_number(number)

    return chat_id, name, number, contact


with open(os.path.join("..", "constants.yaml"), 'r') as ymlfile:
    constants = yaml.load(ymlfile)

rootdir = os.path.join(constants.get("dataDir"), "Takeout", "Hangouts", "Hangouts.json")

with open(rootdir, "r") as source:
    data = json.load(source)
    conversations = data["conversation_state"]
    count = 0
    users = []
    for conversation in conversations:
        #Gets every conversation
        count += 1
        with open("hangouts." + str(count) + ".json", "w") as output:
            json_output = json.dump(conversation, output, sort_keys=True, indent=4)
        participants = conversation.get("conversation_state").get("conversation").get("participant_data")
        #Get participant data
        #for participant in participants:
         #   users.append(get_particpant(participant))
        #messages = conversations.get("event")
        #print(messages)
        for i, event in enumerate(conversations):
            for messages in event:
                for j, message in enumerate(event.get(messages)):
                    for k, text in enumerate(message):
                        print(message.get(text))
                        print(text.get("timestamp"))
                '''
                #TODO Get reciever(s) for each message, right now
                text = message.get("chat_message").get("message_content").get("segment").get("text")
                sender_id = message.get("sender_id").get("chat_id")
                user_id = message.get("self_event_state").get("user_id").get("chat_id")
                sender = [None, None, None, None]
                #for user in users:
                 #   if sender_id == user[0]:
                  #      sender = user
                timestamp = message.get("timestamp")
                date = datetime.datetime.fromtimestamp(timestamp=timestamp)
                Message.insert(type="hangouts", date=date, time=timestamp, sender=sender[1], message=text, contact=sender[3]).execute()
'''
