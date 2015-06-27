__author__ = 'Jacob'
import csv
import os
import yaml
import json
from bs4 import BeautifulSoup
from datetime import datetime

'''
with open("constants.yaml", 'r') as ymlfile:
    constants = yaml.load(ymlfile)
'''

rootdir = os.curdir

'''
<div class="thread"> = a new message group/conversation and names of participants
<div class="message"><div class="message_header"><span class="user"> = Before each person and their response in a thread
<span class="meta"> After above, tells the time for each message
<p> is the actual message after all the above
'''
for file in os.listdir(rootdir):
    if(file.endswith(".htm")):
        #TODO Add more than messages
        if (file=="messages.htm"):
            with open(rootdir + "\\" + file, 'r') as source:
                file_name = os.path.splitext(os.path.basename(file))
                html_file = BeautifulSoup(source.read().decode('utf8', 'ignore'))
                content = html_file.find("div", {"class" : "contents"})
            ###################################################################
            #
            #              Start of FB Message to JSON script
            #
            ###################################################################
                #Get all the threads in content
                threads = content.find_all("div", {"class" : "thread"})
                print threads[0]
                #Now step into each message thread
                for thread in threads:
                    #TODO CHeck to make sure name won't be longer than 256 characters, the Windows limitation
                    output_file_name = thread.string
                    print output_file_name
                    with open(os.path.join('C:\Development\personal_analysis\output', 'facebook.' + output_file_name + '.json'), 'a') as json_output:
                        messages = thread.find_all("div", {"class" : "message"})
                        #Now at the level of each message
                        for message in messages:
                            #user writing the message
                            user = message.find("div", {"class": "user"}).string

                            #time of message
                            #Date and Time
                            date_and_time = message.find("div", {"class": "meta"}).string
                            #TODO split and convert to Date Field
                            time_components = date_and_time.split()
                            print time_components
                            #Converting to proper format for strptime
                            '''
                            if(int(time_components[1]) < 10):
                                date_string = time_components[0] + " 0" + time_components[1] + " " + time_components[2] + " " \
                                              + time_components[3] + time_components[4]
                            else: # NO leading 0 added
                                date_string = time_components[0] + " " + time_components[1] + " " + time_components[2] + " " \
                                              + time_components[3] + time_components[4]
                            #Not using this at the moment, since datetime cannot be serialized to JSON, use date_string instead
                            date_object = datetime.strptime(date_string, '%b %d %Y %I:%M:%f%p')
                            '''

                            #The actual message
                            print message.p
                            print message.p.string
                            text = message.p.string
            ###################################################################
            #
            #              End of FB Message to JSON script
            #
            ###################################################################