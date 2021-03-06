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

import requests
import yaml

# Authentication with Instagram
from insights.io import config

if __name__ != "__main__":
    configuration_files = config.import_yaml_files(".", ["access.yaml"])
    access_config = configuration_files[0]
else:
    configuration_files = config.import_yaml_files("..", ["access.yaml"])
    acces_config = configuration_files[0]

#Based on the get_access_token.py on Instagram's Github
client_id = access_config.get('instagram').get('id')
client_secret = access_config.get('instagram').get('secret')
redirect_uri = access_config.get('instagram').get('redirect')
scope = access_config.get('instagram').get('scope')
# For basic, API seems to need to be set explicitly
if not scope or scope == [""]:
    scope = ["basic"]

authorization_url = "https://api.instagram.com/oauth/authorize/"
payload = {"client_id": client_id, "redirect_uri": redirect_uri, "response_type": "token", "scope": scope}
api_auth = requests.get(authorization_url, params=payload)
api = InstagramAPI(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

#TODO make it so do not have to go to site and then come back
print ("Visit this page and authorize access in your browser: " + redirect_uri)
code = (str(input("Paste in code in query string after redirect: ").strip()))

access_token = api.exchange_code_for_access_token(code)

with open("../access.yaml", 'w') as access:
    access_config.get('instagram').get('token').set(access_token)
    access.write(yaml.dump(access_config, default_flow_style=False))

api = InstagramAPI(access_token=access_token, client_secret=client_secret)
recent_media, next_ = api.user_recent_media(user_id="userid", count=10)