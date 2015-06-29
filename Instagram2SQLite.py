__author__ = 'Jacob'

import os
import peewee
import instagram
from instagram.client import InstagramAPI
from instagram.bind import InstagramAPIError
import yaml

#Authentication with Instagram
with open("access.yaml", 'r') as access:
    access_config = yaml.load(access)


access_token = "YOUR_ACCESS_TOKEN"
client_secret = "YOUR_CLIENT_SECRET"
api = InstagramAPI(access_token=access_token, client_secret=client_secret)
recent_media, next_ = api.user_recent_media(user_id="userid", count=10)