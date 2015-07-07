__author__ = 'Jacob Bieker'

import json
import facebook
import yaml
import os

#Authentication
with open("access.yaml", 'r') as access:
    access_config = yaml.load(access)


#TODO Need to add Facebook login to get Oauth token

token = access_config['facebook']['token']
client_id = access_config['facebook']['clientID']
redirect_uri = access_config['facebook']['redirect']
scopes = access_config['facebook']['scopes']
login_url = 'https://www.facebook.com/dialog/oauth?client_id={'+\
            str(client_id)+'}&redirect_uri={'+\
            str(redirect_uri)+\
            '}&response_type=token&'+\
            'scope={'+str(scopes)+'}'

graph = facebook.GraphAPI(access_token=token)

#Get all friends for a user
friends = graph.get_connections(id='me', connection_name='friends')