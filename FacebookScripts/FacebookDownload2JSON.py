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

# Go through album and extract all the information on the photos inside and return a dictionary
def album2JSON(location):
    '''
    Example Album in photos.htm
    <div class="block"><img src="../../photos/1118349984846132/1118350128179451.jpg" /><div><div class="meta">Tuesday, 23 June 2015 at 20:52 PDT</div>
    <table class="meta"><tr><th>Taken</th><td>1434916977</td></tr><tr><th>Camera Make</th><td></td></tr><tr><th>Orientation</th><td>1</td></tr>
    <tr><th>Exposure</th><td>1/125</td></tr><tr><th>F-Stop</th><td>14/1</td></tr><tr><th>ISO Speed</th><td>400</td></tr><tr><th>Focal length</th>
    <td>28/1</td></tr><tr><th>Upload IP Address</th><td>ADDRESS</td></tr></table><div class="comment"><span class="user">NAME</span>
    Great picture of your mom!!<div class="meta">Tuesday, 23 June 2015 at 23:01 PDT</div></div><div class="comment">
    <span class="user">NAME</span>Sweet kayak!<div class="meta">Thursday, 25 June 2015 at 23:26 PDT</div></div></div></div>
    '''
    with open(link, 'r') as album:
        html_album = BeautifulSoup(album.read().decode('utf-8', 'ignore'))
        content_album = html_album.find("div", {"class": "contents"})
        photos = content_album.find_all("div", {"class": "block"})
        for photo in photos:
            #Work down into the attributes of each photo
            photo_date_and_times = photo.find_all("div", {"class" : "meta"})
            #First one is always the pictures:
            photo_date_and_time = photo_date_and_times[0]

            #Get metadata
            photo_metadata = photo.find('table', {"class": "meta"})
            photo_taken = photo.find('td').text
            camera_make = photo.find('td').text
            photo_orientation = photo.find('td').text
            photo_exposure = photo.find('td').text
            f_stop = photo.find('td').text
            photo_iso = photo.find('td').text
            focal_length = photo.find('td').text

            #Get comments
            photo_comments = photo.find_all("div", {"class": "comment"})
            for comment in photo_comments:
                photo_commenter = comment.find("span", {"class": "user"}).text
                #TODO Check this to make sure it finds the right text
                photo_comment = comment.text
                photo_comment_time = comment.find("div", {"class": "meta"}).text


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
                    #Now step into each album

                    for album in albums:
                        #json_data = []
                        output_file_name += 1
                        with open(os.path.join(rootdir + "\\output", 'facebook.photos.' + str(output_file_name) + '.json'), 'a') as json_output:
                            #Get all links, which includes location of an album index.htm
                            links = album.find_all("a", href=True)
                            for link in links['href']:
                                if link == '*index.htm':
                                    album_location = link
                                    #Now has the location of the album
                                    json_data = album2JSON(link)

                            #Date and Time
                            date_and_times = album.find_all("span", {"class": "meta"}).text
                            album_date_and_time = date_and_times[0]
                            time_components = album_date_and_time.split()
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

            ###################################################################
            #
            #              End of FB Photos to JSON script
            #
            ###################################################################
            ###################################################################
            #
            #              Start of FB Wall to JSON script
            #
            ###################################################################
            ###################################################################
            #
            #              End of FB Wall to JSON script
            #
            ###################################################################