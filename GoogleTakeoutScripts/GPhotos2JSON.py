__author__ = 'Jacob Bieker'
import os
import yaml
import json
from datetime import datetime
import setup

'''
with open("constants.yaml", 'r') as ymlfile:
    constants = yaml.load(ymlfile)
'''

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

