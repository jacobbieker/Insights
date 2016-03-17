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

import os
import peewee
import instagram
from instagram.client import InstagramAPI
from instagram.bind import InstagramAPIError
import yaml

#Authentication with Instagram
# Have to do this because when the command is called from the import in any subfolder it cannot find the dbconfig
if __name__ != "__main__":
    with open(os.path.join("access.yaml"), 'r') as access:
        access_config = yaml.load(access)
else:
    with open(os.path.join("access.yaml"), 'r') as access:
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

with open("../access.yaml", 'w') as access:
    access_config.get('instagram').get('token').set(access_token)
    access.write(yaml.dump(access_config, default_flow_style=False))

api = InstagramAPI(access_token=access_token, client_secret=client_secret)
recent_media, next_ = api.user_recent_media(user_id="userid", count=10)