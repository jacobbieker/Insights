__author__ = 'Jacob'
import csv
import os
import yaml
import json
from bs4 import BeautifulSoup
from datetime import datetime
import exifread
from exifread import *
from glob import glob

'''
with open("constants.yaml", 'r') as ymlfile:
    constants = yaml.load(ymlfile)
'''

rootdir = os.curdir

'''
<div class="thread"> = a new message group/conversation and names of participants
<div class="message"><div class="message_header"><span class="user"> = Before each person and their response in a thread
<span class="meta"> After above, tells the time for each message
<p> is the actual message after all the above <p> is between messages and not part of an actual message div
'''
for file in os.listdir(rootdir + "\\data\\html"):
    if(file.endswith(".htm")):
        #TODO Add more than messages
        if (file=="messages.htm"):
            with open(rootdir + "\\data\\html" + "\\" + file, 'r') as source:
                file_name = os.path.splitext(os.path.basename(file))
                html_file = BeautifulSoup(source.read().decode('utf-8', 'ignore'))
                content = html_file.find("div", {"class" : "contents"})
            ###################################################################
            #
            #              Start of FB Message to JSON script
            #
            ###################################################################
                #Get all the threads in content
                threads = content.find_all("div", {"class" : "thread"})
                output_file_name = 0
                #Now step into each message thread
                for thread in threads:
                    #json_data = []
                    #TODO Check to make sure name won't be longer than 256 characters, the Windows limitation
                    output_file_name += 1
                    with open(os.path.join(rootdir + "\\output", 'facebook.messaging.' + str(output_file_name) + '.json'), 'a') as json_output:
                        messages = thread.find_all("div", {"class" : "message"})
                        #Get all <p> tags, which include the actual content, to iterate throug hand match up with each
                        #message
                        message_content = thread.find_all("p")
                        #TODO Get the list of all paricipants in a thread from the <thread> tag
                        list_of_recipients = []
                        #Now at the level of each message
                        for index, message in enumerate(messages):
                            #print message
                            #user writing the message
                            user = message.find("span", {"class": "user"}).text
                            if(user not in s for s in list_of_recipients):
                                list_of_recipients.append(user)

                            #time of message
                            #Date and Time
                            date_and_time = message.find("span", {"class": "meta"}).text

                            time_components = date_and_time.split()
                            #print time_components
                            #Converting to proper format for strptime
                            if(int(time_components[1]) < 10):
                                date_string = time_components[0] + " 0" + time_components[1] + " " + time_components[2] + " " \
                                              + time_components[3] + " " +time_components[5]
                            else: # NO leading 0 added
                                date_string = time_components[0] + " " + time_components[1] + " " + time_components[2] + " " \
                                              + time_components[3] + " " +time_components[5]
                            #Not using this at the moment, since datetime cannot be serialized to JSON, use date_string instead
                            #Note: Different than GVoice time, different format
                            date_object = datetime.strptime(date_string, '%A, %d %B %Y %H:%M')

                            #The actual message
                            text = message_content[index].text
                            json_output.write("\n")
                            json_data = {'type': 'facebook message',
                                         'time': date_string,
                                         'sender': user,
                                         'recipients': list_of_recipients,
                                         'message': text}
                            json_array = json.dump(json_data, json_output, sort_keys=True, indent=4)
            ###################################################################
            #
            #              End of FB Message to JSON script
            #
            ###################################################################
            ###################################################################
            #
            #              Start of FB Photos to JSON script
            #
            ###################################################################
            if (file=="photos.htm"):
                with open(rootdir + "\\data\\html" + "\\" + file, 'r') as source:
                    file_name = os.path.splitext(os.path.basename(file))
                    html_file = BeautifulSoup(source.read().decode('utf-8', 'ignore'))
                    content = html_file.find("div", {"class" : "contents"})
                    #Get all the albumns in content
                    albums = content.find_all("div", {"class" : "block"})
                    print albums
                    output_file_name = 0
                    #Now step into each message thread
                    for album in albums:
                        #json_data = []
                        output_file_name += 1
                        with open(os.path.join(rootdir + "\\output", 'facebook.photos.' + str(output_file_name) + '.json'), 'a') as json_output:
                            messages = thread.find_all("div", {"class" : "message"})
                            #Get all <p> tags, which include the actual content, to iterate throug hand match up with each
                            #message
                            message_content = thread.find_all("p")
                            list_of_recipients = []
                            #Now at the level of each message
                            for index, message in enumerate(messages):
                                #print message
                                #user writing the message
                                user = message.find("span", {"class": "user"}).text
                                if(user not in s for s in list_of_recipients):
                                    list_of_recipients.append(user)

                                #time of message
                                #Date and Time
                                date_and_time = message.find("span", {"class": "meta"}).text

                                time_components = date_and_time.split()
                                #print time_components
                                #Converting to proper format for strptime
                                if(int(time_components[1]) < 10):
                                    date_string = time_components[0] + " 0" + time_components[1] + " " + time_components[2] + " " \
                                                  + time_components[3] + " " +time_components[5]
                                else: # NO leading 0 added
                                    date_string = time_components[0] + " " + time_components[1] + " " + time_components[2] + " " \
                                                  + time_components[3] + " " +time_components[5]
                                #Not using this at the moment, since datetime cannot be serialized to JSON, use date_string instead
                                #Note: Different than GVoice time, different format
                                date_object = datetime.strptime(date_string, '%A, %d %B %Y %H:%M')

                                #The actual message
                                text = message_content[index].text
                                json_output.write("\n")
                                json_data = {'type': 'facebook message',
                                             'time': date_string,
                                             'sender': user,
                                             'recipients': list_of_recipients,
                                             'message': text}
                                json_array = json.dump(json_data, json_output, sort_keys=True, indent=4)