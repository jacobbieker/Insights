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
__author__ = 'Jacob'
import os
import yaml
from datetime import datetime
from bs4 import BeautifulSoup
from databaseSetup import Message, Voicemail, Call
import databaseSetup

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

with open(os.path.join("..","constants.yaml"), 'r') as ymlfile:
    constants = yaml.load(ymlfile)

rootdir = os.path.join(constants.get('dataDir'), "Takeout", "Voice", "Calls")
# Three lists used to hold output for a peewee many_insert call at the
call_dict = []
text_dict = []
voicemail_dict = []

num_before_insert = 100

# Inserts multiple ones at the same time

def insert_many_queries(call_queries, text_queries, voicemail_queries):
    if len(call_queries) >= num_before_insert:
        Call.insert_many(call_queries).execute()
        #Remove all the stored ones
        del call_dict[:]
        print("Inserted %s or more Calls", num_before_insert)
    if len(text_queries) >= num_before_insert:
        #for text_message in text_queries:
        #    Message.insert(text_message).execute()
        Message.insert_many(text_queries).execute()
        del text_dict[:]
        print("Inserted %s or more Texts", num_before_insert)
    if len(voicemail_queries) >= num_before_insert:
        Voicemail.insert_many(voicemail_queries).execute()
        del voicemail_dict[:]
        print("Inserted %s or more Voicemails", num_before_insert)

def voicemail2SQLite(caller, number, time, message):
    #contact = databaseSetup.get_contact_by_number(number)
    voicemail_dict.append({'date': time, 'caller': caller, 'message': message})

def text2SQLite(sender, reciever, time, number, message):
    #contact = databaseSetup.get_contact_by_number(number)
    text_dict.append({'date': time, 'type': 'sms', 'sender': sender, 'reciever': reciever, 'message': message})

def call2SQLite(caller, status, time, duration, number):
    #contact = databaseSetup.get_contact_by_number(number)
    call_dict.append({'date': time, 'caller': caller, 'reciever': 'Me', 'answered': status, 'length': duration})

'''
SAMPLE INPUT:
<div class="message"><abbr class="dt" title="2012-01-16T05:48:34.273Z">Jan 16, 2012, 5:48:34 AM
GMT</abbr>:
<cite class="sender vcard"><a class="tel" href="tel:+15038547254"><span class="fn">+15038547254</span></a></cite>:
<q>goodnight:) sweet dreams my darling:)</q></div>
'''
conversation_number = 1  # Track conversation number, for continuity
for file in os.listdir(rootdir):
    insert_many_queries(call_dict, text_dict, voicemail_dict)
    if file.endswith(".html"):
        with open(os.path.join(rootdir, file), 'r', encoding='latin-1') as source:
            file_name = os.path.splitext(os.path.basename(file))
            yaml_file_name = file_name[0].split(" -")
            html_file = BeautifulSoup(source.read())
            ###################################################################
            #
            #              Start of SMS to yaml script
            #
            ###################################################################
            if (yaml_file_name[1] == ' Text'):
                messages = html_file.find_all("div", {"class": "message"})
                with open(os.path.join(constants.get('outputDir'), 'gvoice.' + str(yaml_file_name[0]) + '.yaml'), 'a') as yaml_output:
                    yaml_data = []
                    for message in messages:
                        # Date and Time
                        date_and_time = message.abbr.text
                        # TODO split and convert to Date Field
                        time_components = date_and_time.split()
                        time_components[1] = time_components[1][:-1]
                        time_components[2] = time_components[2][:-1]
                        # Converting to proper format for strptime
                        if (int(time_components[1]) < 10):
                            date_string = time_components[0] + " 0" + time_components[1] + " " + time_components[
                                2] + " " \
                                          + time_components[3] + time_components[4]
                        else:  # NO leading 0 added
                            date_string = time_components[0] + " " + time_components[1] + " " + time_components[2] + " " \
                                          + time_components[3] + time_components[4]
                        # Not using this at the moment, since datetime cannot be serialized to yaml, use date_string instead
                        date_object = datetime.strptime(date_string, '%b %d %Y %I:%M:%f%p')

                        # Get sender
                        sender = message.cite.text

                        # Telephone
                        gvoice_number = message.a.get('href')
                        phone_number = gvoice_number.split(':')

                        # SMS
                        text = message.q.text

                        # Get reciever:
                        if (sender != 'Me'):
                            reciever = 'Me'
                        else:
                            reciever = yaml_file_name[0]
                        yaml_data.append({'type': 'sms',
                                          'time': date_string,
                                          'conversation': conversation_number,
                                          'sender': sender,
                                          'reciever': reciever,
                                          'phone number': phone_number[1],
                                          'message': text})
                        text2SQLite(sender, reciever, date_string, phone_number[1], text)
                    yaml_array = yaml.dump(yaml_data, yaml_output, default_flow_style=False)
            conversation_number += 1  # increase, as each HTML file with Text is one conversation
            ###################################################################
            #
            #              End of SMS to yaml script
            #
            ###################################################################
            ###################################################################
            #
            #              Start of Call to yaml script
            #
            ###################################################################
            if (yaml_file_name[1] == ' Missed' or yaml_file_name[1] == ' Recieved' or yaml_file_name[1] == ' Placed'):
                calls = html_file.find_all("div", {"class": "haudio"})
                with open(os.path.join(constants.get('outputDir'), 'gvoice.' + str(yaml_file_name[0]) + '.yaml'), 'a') as yaml_output:
                    yaml_data = []
                    for call in calls:
                        # Date and Time
                        date_and_time = call.abbr.text
                        # TODO split and convert to Date Field
                        time_components = date_and_time.split()
                        time_components[1] = time_components[1][:-1]
                        time_components[2] = time_components[2][:-1]
                        # Converting to proper format for strptime
                        if (int(time_components[1]) < 10):
                            date_string = time_components[0] + " 0" + time_components[1] + " " + time_components[
                                2] + " " \
                                          + time_components[3] + time_components[4]
                        else:  # NO leading 0 added
                            date_string = time_components[0] + " " + time_components[1] + " " + time_components[2] + " " \
                                          + time_components[3] + time_components[4]
                        # Not using this at the moment, since datetime cannot be serialized to yaml, use date_string instead
                        date_object = datetime.strptime(date_string, '%b %d %Y %I:%M:%f%p')
                        # Get caller
                        if (len(call.find_all("span", {"class": "fn"})) >= 1):
                            caller = call.find_all("span", {"class": "fn"})[1].text

                        # Telephone
                        gvoice_number = call.a.get('href')
                        phone_number = gvoice_number.split(':')

                        # Call length
                        if (len(call.find_all("abbr", {"class": "duration"})) >= 1):
                            duration = call.find_all("abbr", {"class": "duration"})[0].text

                        else:
                            duration = None

                        # Call type: Missed, Placed, or Recieved
                        status = yaml_file_name[1].strip(" ")
                        yaml_data.append({'type': 'call',
                                          'status': status,
                                          'time': date_string,
                                          'caller': caller,
                                          'duration': duration,
                                          'phone number': phone_number[1]})
                        call2SQLite(caller=caller, status=status, time=date_string, duration=duration, number=phone_number[1])
                    yaml_array = yaml.dump(yaml_data, yaml_output, default_flow_style=False)
            ###################################################################
            #
            #              End of Call to yaml script
            #
            ###################################################################
            ###################################################################
            #
            #              Start of Voicemail to yaml script
            #
            ###################################################################
            if (yaml_file_name[1] == ' Voicemail'):
                voicemails = html_file.find_all("div", {"class": "haudio"})
                with open(os.path.join(constants.get('outputDir'), 'gvoice.' + str(yaml_file_name[0]) + '.yaml'), 'a') as yaml_output:
                    yaml_data = []
                    for voicemail in voicemails:
                        # Date and Time
                        date_and_time = voicemail.abbr.text

                        # TODO split and convert to Date Field
                        time_components = date_and_time.split()
                        time_components[1] = time_components[1][:-1]
                        time_components[2] = time_components[2][:-1]
                        # Converting to proper format for strptime
                        if (int(time_components[1]) < 10):
                            date_string = time_components[0] + " 0" + time_components[1] + " " + time_components[
                                2] + " " \
                                          + time_components[3] + time_components[4]
                        else:  # NO leading 0 added
                            date_string = time_components[0] + " " + time_components[1] + " " + time_components[2] + " " \
                                          + time_components[3] + time_components[4]
                        # Not using this at the moment, since datetime cannot be serialized to yaml, use date_string instead
                        date_object = datetime.strptime(date_string, '%b %d %Y %I:%M:%f%p')

                        # Get caller
                        if (len(voicemail.find_all("span", {"class": "fn"})) >= 1):
                            caller = voicemail.find_all("span", {"class": "fn"})[1].text

                        # Telephone
                        gvoice_number = voicemail.a.get('href')
                        phone_number = gvoice_number.split(':')

                        # Voicemail text
                        if (len(voicemail.find_all("span", {"class": "full-text"})) >= 1):
                            text = voicemail.find_all("span", {"class": "full-text"})[0].text

                        # Voicemail length
                        if (len(voicemail.find_all("abbr", {"class": "duration"})) >= 1):
                            duration = voicemail.find_all("abbr", {"class": "duration"})[0].text

                        yaml_data.append({'type': 'voicemail',
                                          'time': date_string,
                                          'caller': caller,
                                          'duration': duration,
                                          'phone number': phone_number[1],
                                          'message': text})
                        voicemail2SQLite(caller=caller, number=phone_number[1], time=date_string, message=text)
                    yaml_array = yaml.dump(yaml_data, yaml_output, default_flow_style=False)
                    ###################################################################
                    #
                    #              End of Voicemail to yaml script
                    #
                    ###################################################################
# Insert any remaining entries
if len(call_dict) != 0:
    Call.insert_many(call_dict)
if len(text_dict) != 0:
    Message.insert_many(text_dict)
if len(voicemail_dict) != 0:
    Voicemail.insert_many(voicemail_dict)