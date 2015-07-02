__author__ = 'Jacob'
import os
import yaml
import flickrapi
import json

#Authentication
with open("access.yaml", 'r') as access:
    access_config = yaml.load(access)

key = access_config['flickr']['key']
secret = access_config['flickr']['secret']

flickr = flickrapi.FlickrAPI(key, secret)