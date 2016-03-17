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
__author__ = 'Jacob Bieker'

import json
import facebook
import yaml
import os

#Authentication
# Have to do this because when the command is called from the import in any subfolder it cannot find the dbconfig
if __name__ == "__main__":
    with open(os.path.join("access.yaml"), 'r') as access:
        access_config = yaml.load(access)
else:
    with open(os.path.join("access.yaml"), 'r') as access:
        access_config = yaml.load(access)


#TODO Need to add Facebook login to get Oauth token

token = access_config.get('facebook').get('token')
client_id = access_config.get('facebook').get('clientID')
redirect_uri = access_config.get('facebook').get('redirect')
scopes = access_config.get('facebook').get('scopes')
login_url = 'https://www.facebook.com/dialog/oauth?client_id={'+\
            str(client_id)+'}&redirect_uri={'+\
            str(redirect_uri)+\
            '}&response_type=token&'+\
            'scope={'+str(scopes)+'}'

graph = facebook.GraphAPI(access_token=token)

#Get all friends for a user
friends = graph.get_connections(id='me', connection_name='friends')