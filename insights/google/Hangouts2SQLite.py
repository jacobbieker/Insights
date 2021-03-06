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

from insights.config import databaseSetup
from insights.config.databaseSetup import Contacts, Message, Voicemail

'''
The article included in this repository is licensed under a Attribution-NonCommercial-ShareAlike 3.0 license, meaning that you are free to copy, distribute, transmit and adapt this work for non-commercial use, but that you must credit Fabian Mueller as the original author of the piece, and provide a link to the source: https://bitbucket.org/dotcs/hangouts-log-reader/
'''


class Participant(object):
    """
    Participant class.
    """

    def __init__(self, gaia_id, chat_id, name, phone):
        """
        Constructor
        """
        self.name = name
        self.phone = phone
        self.gaia_id = gaia_id
        self.chat_id = chat_id

    def get_id(self):
        """
        Getter for the internal Google ID of the participant.

        @return internal Google participant id
        """
        return self.gaia_id

    def get_phone(self):
        """
        Getter for the phone of a participant.

        @return phone of the participant (may be None)
        """
        return self.phone

    def get_name(self):
        """
        Getter for the name of a participant.

        @return name of the participant (may be None)
        """
        return self.name

    def __str__(self):
        """
        @return name of the participant or its id if name is None
        """
        if self.get_name() is None:
            if self.get_phone() is None:
                return self.get_id()
            else:
                return self.get_phone()
        else:
            # return "%s <%s>" % (self.get_name(), self.get_id())
            return self.get_name()


class ParticipantList(object):
    """
    List class for participants.
    """

    def __init__(self):
        """
        Constructor
        """
        self.p_list = {}
        self.current_iter = 0
        self.max_iter = 0

    def add(self, p):
        """
        Adds a participant to the list.

        @return the participant list
        """
        self.p_list[p.get_id()] = p
        return self.p_list

    def get_by_id(self, id):
        """
        Queries a participant by its id.

        @return the participant or None if id is not listed
        """
        try:
            return self.p_list[id]
        except:
            return None

    def get_recievers_id(self, id):
        """
        Queries a list of participants excluding one

        @:return the list of participants
        """
        try:
            recievers = [p for p in self.p_list if p.get_id() != id]
            return recievers
        except:
            return self.p_list

    def __iter__(self):
        self.current_iter = 0
        self.max_iter = len(self.p_list) - 1
        return self

    def __next__(self):
        if self.current_iter > self.max_iter:
            raise StopIteration
        else:
            self.current_iter += 1
            return self.p_list.values()[self.current_iter - 1]

    def __str__(self):
        """
        @return names of the participants seperated by a comma
        """
        string = ""
        for p in self.p_list.values():
            string += str(p) + ", "
        return string[:-2]


class Event(object):
    """
    Event class.
    """

    def __init__(self, event_id, sender_id, timestamp, message, event_type):
        """
        Constructor
        """
        self.event_id = event_id
        self.sender_id = sender_id
        self.timestamp = timestamp
        self.message = message
        self.event_type = event_type

    def get_id(self):
        """
        Getter method for the id.

        @return event id
        """
        return self.event_id

    def get_sender_id(self):
        """
        Getter method for the sender id.

        @return sender id of the event
        """
        return self.sender_id

    def get_type(self):
        """
        Getter method for the sender id.

        @return reciever ids of the event
        """
        return self.event_type

    def get_timestamp(self):
        """
        Getter method for the timestamp.

        @return timestamp of the event
        """
        return self.timestamp

    def get_message(self):
        """
        Getter method for the message.

        @return message (list)
        """
        return self.message

    def get_picture(self):
        """
        Getter method for the picture.

        @return picture (url)
        """
        return self.message

    def get_formatted_message(self):
        """
        Getter method for a formatted message (the messages are joined by a space).

        @return message (string)
        """
        string = ""
        for m in self.message:
            string += str(m) + " "
        return string[:-1]


class EventList(object):
    """
    Event list class
    """

    def __init__(self):
        """
        Constructor
        """
        self.event_list = {}
        self.current_iter = 0
        self.max_iter = 0

    def add(self, e):
        """
        Adds an event to the event list

        @return event list
        """
        self.event_list[e.get_id()] = e
        return self.event_list

    def get_by_id(self, id):
        """
        Getter method for an event by its id.

        @returns event
        """
        try:
            return self.event_list[id]
        except:
            return None

    def __iter__(self):
        self.current_iter = 0
        self.max_iter = len(self.event_list) - 1
        return self

    def __next__(self):
        if self.current_iter > self.max_iter:
            raise StopIteration
        else:
            self.current_iter += 1
            return list(self.event_list.values())[self.current_iter - 1]


class Conversation(object):
    """
    Conversation class
    """

    def __init__(self, conversation_id, timestamp, participants, events):
        """
        Constructor
        """
        self.conversation_id = conversation_id
        self.timestamp = timestamp
        self.participants = participants
        self.events = events

    def __str__(self):
        """
        Prints to string
        """
        return self.conversation_id

    def get_id(self):
        """
        Getter method for the conversation id

        @return conversation id
        """
        return self.conversation_id

    def get_timestamp(self):
        """
        Getter method for the timestamp

        @return timestamp
        """
        return self.timestamp

    def get_participants(self):
        """
        Getter method for the participants.

        @return participants of the conversation
        """
        return self.participants

    def get_events(self):
        """
        Getter method for the sorted events.

        @return events of the conversation (sorted)
        """
        return sorted(self.events, key=lambda event: event.get_timestamp())

    def get_events_unsorted(self):
        """
        Getter method for the unsorted events.

        @return events of the conversation (unsorted)
        """
        return self.events


def parse_json_file(filename):
    """
    Parses the json file.

    @return Array of Conversations
    """

    conversation_list = []
    count = 0
    with open(filename, encoding="utf-8", errors='ignore') as json_data:
        data = json.load(json_data)

        for conversation in data["conversation_state"]:
            conversation_data = extract_conversation_data(conversation)
            conversation_list.append(conversation_data)
            count += 1
            with open(os.path.join(outputdir, "hangouts." + str(count) + ".json"), "w") as dump:
                json_dump = json.dump(conversation, fp=dump, indent=4, sort_keys=True)

    return conversation_list


def extract_conversation_data(conversation):
    """
    Extracts the data that belongs to a single conversation.

    @return Conversation object
    """
    try:
        # note the initial timestamp of this conversation
        initial_timestamp = conversation["response_header"]["current_server_time"]
        conversation_id = conversation["conversation_id"]["id"]

        # find out the participants
        participant_list = ParticipantList()
        for participant in conversation["conversation_state"]["conversation"]["participant_data"]:
            gaia_id = participant["id"]["gaia_id"]
            chat_id = participant["id"]["chat_id"]
            try:
                name = participant["fallback_name"]
            except KeyError:
                name = None
            try:
                phone = participant["phone_number"]["e164"]
            except KeyError:
                phone = None
            p = Participant(gaia_id, chat_id, name, phone)
            participant_list.add(p)

        event_list = EventList()

        for event in conversation["conversation_state"]["event"]:
            event_id = event["event_id"]
            sender_id = event["sender_id"]  # has dict values "gaia_id" and "chat_id"
            timestamp = event["timestamp"]
            event_type = event["event_type"]
            text = list()
            try:
                message_content = event["chat_message"]["message_content"]
                try:
                    for segment in message_content["segment"]:
                        if segment["type"].lower() in ("TEXT".lower(), "LINK".lower()):
                            text.append(segment["text"])
                except KeyError:
                    pass  # may happen when there is no (compatible) attachment
                try:
                    for attachment in message_content["attachment"]:
                        # if there is a Google+ photo attachment we append the URL
                        if attachment["embed_item"]["type"][0].lower() == "PLUS_PHOTO".lower():
                            text.append(attachment["embed_item"]["embeds.PlusPhoto.plus_photo"]["url"])
                except KeyError:
                    pass  # may happen when there is no (compatible) attachment
            except KeyError:
                continue  # that's okay
            # finally add the event to the event list
            event_list.add(Event(event_id, sender_id["gaia_id"], timestamp, text, event_type))
    except KeyError:
        raise RuntimeError("The conversation data could not be extracted.")
    return Conversation(conversation_id, initial_timestamp, participant_list, event_list)


def print_conversation(conversation):
    """
    Prints conversations in human readable format.

    @return None
    """
    participants = conversation.get_participants()
    for event in conversation.get_events():
        author = "<UNKNOWN>"
        author_id = participants.get_by_id(event.get_sender_id())
        if author_id:
            author = author_id.get_name()
        print("%(timestamp)s: <%(author)s> %(message)s" % \
              {
                  "timestamp": event.get_timestamp(),
                  "author": author,
                  "message": event.get_formatted_message(),
              })


from insights.io import config

if __name__ != "__main__":
    configuration_files = config.import_yaml_files(".", ["constants"])
    constants = configuration_files[0]
else:
    configuration_files = config.import_yaml_files("..", ["constants"])
    constants = configuration_files[0]

rootdir = os.path.join(constants.get("dataDir"), "Takeout", "Hangouts", "Hangouts.json")
outputdir = os.path.join(constants.get("outputDir"))

print("Starting Google Hangout Parsing")
conversations = parse_json_file(rootdir)
message_list = []
for conversation in conversations:
    # print(conversation.get_timestamp())
    print("conversation id: %s, participants: %s" % (conversation.get_id(), str(conversation.get_participants())))
    # print_conversation(conversation)
    # Need to save to the database
    for event in conversation.get_events():
        participants = conversation.get_participants()
        recievers = participants.get_recievers_id(event.get_sender_id())
        list_of_recievers = str(recievers)
        event_type = event.get_type()
        message = str(event.get_formatted_message())
        sender = participants.get_by_id(event.get_sender_id())
        sender_name = str(sender)
        if str(event_type) == "VOICEMAIL":
            Voicemail.insert({'date': event.get_timestamp(), 'caller': sender_name,
                              'message': message}).execute()
        elif str(event_type) == "SMS":
            Message.insert({'date': event.get_timestamp(), 'type': 'sms',
                            'sender': sender_name, 'reciever': list_of_recievers,
                            'message': message}).execute()
        elif str(event_type) == "REGULAR_CHAT_MESSAGE":
            Message.insert({'date': event.get_timestamp(), 'type': 'hangouts',
                            'sender': sender_name, 'reciever': list_of_recievers,
                            'message': message}).execute()
        else:
            print("Event Type not Recognized: " + str(event_type))


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
