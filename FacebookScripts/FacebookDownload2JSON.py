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
import setup
import re

'''
with open("constants.yaml", 'r') as ymlfile:
    constants = yaml.load(ymlfile)
'''

rootdir = os.curdir

#Date and Time, Facebook Format
def get_date_and_time(time_string):
    time_components = time_string.split()
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
    return date_string

# Go through album and extract all the information on the photos inside and return a dictionary
def album2JSON(location, album_name):
    '''
    Example Album in photos.htm
    <div class="block"><img src="../../photos/1118349984846132/1118350128179451.jpg" /><div><div class="meta">Tuesday, 23 June 2015 at 20:52 PDT</div>
    <table class="meta"><tr><th>Taken</th><td>1434916977</td></tr><tr><th>Camera Make</th><td></td></tr><tr><th>Orientation</th><td>1</td></tr>
    <tr><th>Exposure</th><td>1/125</td></tr><tr><th>F-Stop</th><td>14/1</td></tr><tr><th>ISO Speed</th><td>400</td></tr><tr><th>Focal length</th>
    <td>28/1</td></tr><tr><th>Upload IP Address</th><td>ADDRESS</td></tr></table><div class="comment"><span class="user">NAME</span>
    Great picture of your mom!!<div class="meta">Tuesday, 23 June 2015 at 23:01 PDT</div></div><div class="comment">
    <span class="user">NAME</span>Sweet kayak!<div class="meta">Thursday, 25 June 2015 at 23:26 PDT</div></div></div></div>
    '''
    with open(location, 'r') as album:
        html_album = BeautifulSoup(album.read().decode('utf-8', 'ignore'))
        content_album = html_album.find("div", {"class": "contents"})
        photos = content_album.find_all("div", {"class": "block"})
        output_file_name = 0
        for photo in photos:
            output_file_name += 1
            with open(os.path.join(setup.OUT_PATH, "facebook." + str(album_name) + ".photo." + str(output_file_name) + ".json"), 'a') as json_output:
                #Work down into the attributes of each photo
                photo_date_and_times = photo.find_all("div", {"class" : "meta"})
                #First one is always the pictures:
                photo_date_and_time = photo_date_and_times[0]

                date_string = get_date_and_time(photo_date_and_time)

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
                    photo_comment_time = get_date_and_time(comment.find("div", {"class": "meta"}).text)
                    json_output.write(",\n")
                    json_data = {'type': 'facebook album photo',
                                 'album': album_name,
                                 'time': date_string,
                                 'taken': photo_taken,
                                 'camera': camera_make,
                                 'orientation': photo_orientation,
                                 'exposure': photo_exposure,
                                 'f-stop': f_stop,
                                 'iso': photo_iso,
                                 'focal length': focal_length,
                                 'commenter': photo_commenter,
                                 'comment time': photo_comment_time,
                                 'comment': photo_comment}
                    json_array = json.dump(json_data, json_output, sort_keys=True, indent=4)

def thread2JSON(output_name, thread):
    with open(os.path.join(setup.OUT_PATH, 'facebook.messaging.' + str(output_name) + '.json'), 'a') as json_output:
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

            date_and_time = message.find("span", {"class": "meta"}).text
            date_string = get_date_and_time(date_and_time)

            #The actual message
            text = message_content[index].text
            if (output_name != 1):
                json_output.write(",\n")
            json_data = {'type': 'facebook message',
                         'time': date_string,
                         'sender': user,
                         'recipients': list_of_recipients,
                         'message': text}
            json_array = json.dump(json_data, json_output, sort_keys=True, indent=4)

def wall_post2JSON(wall_post, output_name):
    #Expects a beautifulSoup that includes the following setup, parses to JSON
    '''
    <p><div class="meta">Thursday, 10 November 2011 at 20:41 PST</div>NAME wrote on your timeline.<div class="comment">http://dictionary.reference.com/browse/dragon
    check the pronunciation</div></p>
    '''
    with open(os.path.join(setup.OUT_PATH, 'facebook.wall.' + str(output_name) +'.json'), 'a'):
        date_string = get_date_and_time(wall_post.find("div", {"class": "meta"}).text)
        writers = wall_post.text # get text between date_string and </p>

        #Regex below for the different possibilities:
        re_post = re.compile("wrote on your timeline")
        re_life_event = re.compile("added a life event: *")
        re_changed_event = re.compile("changed *")
        re_edited_event = re.compile("edited *")
        re_friends = re.compile("are now friends")
        re_new_relationship = re.compile("now in a relationship")
        re_changed_relationship = re.compile("went from being *")
        re_status = re.compile("updated his status")
        re_photo = re.compile("added a new photo to the album *")
        re_participants = re.compile("Jacob Bieker and *\s*\s$") #get the two participants if they exist

        #Now check if any of the above are in the text, and diff category for each
        participants = writers.re.match(re_participants)
        if  participants:
            split_people = participants.group().split(" ")
            other_person = split_people[3, ] #all names after "and"
        else:
            other_person = ""

        #Check for ones with wildcard
        life_event = writers.search(re_life_event)
        changed_event = writers.search(re_changed_event)
        edited_event = writers.search(re_edited_event)
        change_relationship = writers.search(re_changed_relationship)
        photo = writers.search(re_photo)

        if life_event:


        #Now check the true/false event types
        if writers.search(re_post):
            event_type = "wall post"
        elif writers.search(re_friends):
            event_type = "friendship"
        elif writers.search(re_status):
            event_type = "status update"
        elif writers.search(re_new_relationship):
            event_type = "start relationship"

        post = wall_post.find("div", {"class": "comment"})

'''
<div class="thread"> = a new message group/conversation and names of participants
<div class="message"><div class="message_header"><span class="user"> = Before each person and their response in a thread
<span class="meta"> After above, tells the time for each message
<p> is the actual message after all the above <p> is between messages and not part of an actual message div
'''
for file in os.listdir(setup.DATA_PATH + "\\html"):
    if(file.endswith(".htm")):
        if (file=="messages.htm"):
            with open(setup.DATA_PATH + "\\html" + "\\" + file, 'r') as source:
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
                    thread2JSON(output_file_name, thread)
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
                with open(setup.DATA_PATH +"\\html" + "\\" + file, 'r') as source:
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
                        #Get all links, which includes location of an album index.htm
                        links = album.find_all("a", href=True)
                        for link in links['href']:
                            if link == '*index.htm':
                                album_location = link
                                album_name = link.text
                                #Now has the location of the album
                                album2JSON(album_location, album_name)
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