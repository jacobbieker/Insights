__author__ = 'Jacob'
import os
import yaml
import flickrapi
import json
import webbrowser

#Authentication
with open("access.yaml", 'r') as access:
    access_config = yaml.load(access)

key = access_config['flickr']['key']
secret = access_config['flickr']['secret']
permissions = access_config['flickr']['permissions']

#Get response as unparsed JSON to store
flickr = flickrapi.FlickrAPI(key, secret, format='json')

# Only do this if we don't have a valid token already
if not flickr.token_valid(perms=permissions):

    # Get a request token
    flickr.get_request_token(oauth_callback='oob')

    # Open a browser at the authentication URL. Do this however
    # you want, as long as the user visits that URL.
    authorize_url = flickr.auth_url(perms=permissions)
    webbrowser.open_new_tab(authorize_url)

    # Get the verifier code from the user. Do this however you
    # want, as long as the user gives the application the code.
    verifier = unicode(raw_input('Verifier code: '))

    # Trade the request token for an access token
    flickr.get_access_token(verifier)
