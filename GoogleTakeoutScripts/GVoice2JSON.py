__author__ = 'Jacob'
import os
from bs4 import BeautifulSoup
import json
import yaml
from datetime import datetime

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree
'''
with open("constants.yaml", 'r') as ymlfile:
    constants = yaml.load(ymlfile)
'''
rootdir = "C:\Users\jacob_000\OneDrive\Personal_Projects\Takeout\Voice\Calls"

'''
SAMPLE INPUT:
<div class="message"><abbr class="dt" title="2012-01-16T05:48:34.273Z">Jan 16, 2012, 5:48:34 AM
GMT</abbr>:
<cite class="sender vcard"><a class="tel" href="tel:+15038547254"><span class="fn">+15038547254</span></a></cite>:
<q>goodnight:) sweet dreams my darling:)</q></div>
'''
for file in os.listdir(rootdir):
    if file.endswith(".html"):
        with open(rootdir + "\\" + file, 'r') as source:
            file_name = os.path.splitext(os.path.basename(file))
            json_file_name = file_name[0].split(" -")
            html_file = BeautifulSoup(source.read().decode('utf8', 'ignore'))
            ###################################################################
            #
            #              Start of SMS to JSON script
            #
            ###################################################################
            if(json_file_name[1] == ' Text'):
                messages = html_file.find_all("div", { "class" : "message"})
                with open(os.path.join('C:\Development\personal_analysis\output', 'gvoice.' + json_file_name[0] + '.json'), 'a') as json_output:
                    for message in messages:
                        #Date and Time
                        date_and_time = message.abbr.string
                        #TODO split and convert to Date Field
                        time_components = date_and_time.split()
                        time_components[1] = time_components[1][:-1]
                        time_components[2] = time_components[2][:-1]
                        #Converting to proper format for strptime
                        if(int(time_components[1]) < 10):
                            date_string = time_components[0] + " 0" + time_components[1] + " " + time_components[2] + " " \
                                          + time_components[3] + time_components[4]
                        else: # NO leading 0 added
                            date_string = time_components[0] + " " + time_components[1] + " " + time_components[2] + " " \
                                          + time_components[3] + time_components[4]
                        #Not using this at the moment, since datetime cannot be serialized to JSON, use date_string instead
                        date_object = datetime.strptime(date_string, '%b %d %Y %I:%M:%f%p')

                        #Get sender
                        sender = message.cite.string

                        #Telephone
                        gvoice_number = message.a.get('href')
                        phone_number = gvoice_number.split(':')

                        #SMS
                        text = message.q.string

                        #Get reciever:
                        if(sender != 'Me'):
                            reciever = 'Me'
                        else:
                            reciever = json_file_name[0]

                        json_data = {'type': 'sms',
                                     'time': date_string,
                                     'sender': sender,
                                     'reciever': reciever,
                                     'phone number': phone_number[1],
                                     'message': text}
                        json_array = json.dump(json_data, json_output, sort_keys=True, indent=4)
            ###################################################################
            #
            #              End of SMS to JSON script
            #
            ###################################################################
            ###################################################################
            #
            #              Start of Call to JSON script
            #
            ###################################################################
            if(json_file_name[1] == ' Missed' or json_file_name[1] == ' Recieved' or json_file_name[1] == ' Placed'):
                calls = html_file.find_all("div", { "class" : "haudio"})
                with open(os.path.join('C:\Development\personal_analysis\output', 'gvoice.' + json_file_name[0] + '.json'), 'a') as json_output:
                    for call in calls:
                        #Date and Time
                        date_and_time = call.abbr.string
                        #TODO split and convert to Date Field
                        time_components = date_and_time.split()
                        time_components[1] = time_components[1][:-1]
                        time_components[2] = time_components[2][:-1]
                        #Converting to proper format for strptime
                        if(int(time_components[1]) < 10):
                            date_string = time_components[0] + " 0" + time_components[1] + " " + time_components[2] + " " \
                                          + time_components[3] + time_components[4]
                        else: # NO leading 0 added
                            date_string = time_components[0] + " " + time_components[1] + " " + time_components[2] + " " \
                                          + time_components[3] + time_components[4]
                        #Not using this at the moment, since datetime cannot be serialized to JSON, use date_string instead
                        date_object = datetime.strptime(date_string, '%b %d %Y %I:%M:%f%p')

                        #Get caller
                        if (len(call.find_all("span", { "class" : "fn"})) >=1):
                            caller = call.find_all("span", { "class" : "fn"})[1].string

                        #Telephone
                        gvoice_number = call.a.get('href')
                        phone_number = gvoice_number.split(':')

                        #Call length
                        if(len(call.find_all("abbr", {"class" : "duration"})) >= 1):
                            duration = call.find_all("abbr", {"class" : "duration"})[0].string
                        else:
                            duration = None

                        #Call type: Missed, Placed, or Recieved
                        status = json_file_name[1].strip(" ")

                        json_data = {'type': 'call',
                                     'status': status,
                                     'time': date_string,
                                     'caller': caller,
                                     'duration': duration,
                                     'phone number': phone_number[1]}
                        json_array = json.dump(json_data, json_output, sort_keys=True, indent=4)
            ###################################################################
            #
            #              End of Call to JSON script
            #
            ###################################################################
            ###################################################################
            #
            #              Start of Voicemail to JSON script
            #
            ###################################################################
            if(json_file_name[1] == ' Voicemail'):
                voicemails = html_file.find_all("div", { "class" : "haudio"})
                with open(os.path.join('C:\Development\personal_analysis\output', 'gvoice.' + json_file_name[0] + '.json'), 'a') as json_output:
                    for voicemail in voicemails:
                        #Date and Time
                        date_and_time = voicemail.abbr.string
                        #TODO split and convert to Date Field
                        time_components = date_and_time.split()
                        time_components[1] = time_components[1][:-1]
                        time_components[2] = time_components[2][:-1]
                        #Converting to proper format for strptime
                        if(int(time_components[1]) < 10):
                            date_string = time_components[0] + " 0" + time_components[1] + " " + time_components[2] + " " \
                                          + time_components[3] + time_components[4]
                        else: # NO leading 0 added
                            date_string = time_components[0] + " " + time_components[1] + " " + time_components[2] + " " \
                                          + time_components[3] + time_components[4]
                        #Not using this at the moment, since datetime cannot be serialized to JSON, use date_string instead
                        date_object = datetime.strptime(date_string, '%b %d %Y %I:%M:%f%p')

                        #Get caller
                        if (len(voicemail.find_all("span", { "class" : "fn"})) >=1):
                            caller = voicemail.find_all("span", { "class" : "fn"})[1].string

                        #Telephone
                        gvoice_number = voicemail.a.get('href')
                        phone_number = gvoice_number.split(':')

                        #Voicemail text
                        if (len(voicemail.find_all("span", { "class" : "full-text"})) >= 1):
                            text = voicemail.find_all("span", { "class" : "full-text"})[0].string

                        #Voicemail length
                        if(len(voicemail.find_all("abbr", {"class" : "duration"})) >= 1):
                            duration = voicemail.find_all("abbr", {"class" : "duration"})[0].string

                        json_data = {'type': 'voicemail',
                                     'time': date_string,
                                     'caller': caller,
                                     'duration': duration,
                                     'phone number': phone_number[1],
                                     'message': text}
                        json_array = json.dump(json_data, json_output, sort_keys=True, indent=4)
            ###################################################################
            #
            #              End of Voicemail to JSON script
            #
            ###################################################################