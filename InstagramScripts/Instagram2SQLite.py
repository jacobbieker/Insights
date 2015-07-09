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

#Based on the get_access_token.py on Instagram's Github
client_id = access_config.get('instagram').get('id')
client_secret = access_config.get('instagram').get('secret')
redirect_uri = access_config.get('instagram').get('redirect')
scope = access_config.get('instagram').get('scope')
# For basic, API seems to need to be set explicitly
if not scope or scope == [""]:
    scope = ["basic"]

api = InstagramAPI(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
redirect_uri = api.get_authorize_login_url(scope = scope)

#TODO make it so do not have to go to site and then come back
print ("Visit this page and authorize access in your browser: "+ redirect_uri)
code = (str(input("Paste in code in query string after redirect: ").strip()))

access_token = api.exchange_code_for_access_token(code)

with open("access.yaml", 'w') as access:
    access_config.get('instagram').get('token').set(access_token)
    access.write(yaml.dump(access_config, default_flow_style=False))

api = InstagramAPI(access_token=access_token, client_secret=client_secret)
recent_media, next_ = api.user_recent_media(user_id="userid", count=10)