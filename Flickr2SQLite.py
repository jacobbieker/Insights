__author__ = 'Jacob Bieker'
import os
import yaml
import flickrapi
import json
import webbrowser
import setup

#Authentication
with open("access.yaml", 'r') as access:
    access_config = yaml.load(access)

key = access_config['flickr']['key']
secret = access_config['flickr']['secret']
permissions = access_config['flickr']['permissions']
extras = access_config['flickr']['extras']

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
    token = flickr.get_access_token(verifier)
    print token

#Go through photos
for photo in flickr.walk_photosets(extras=extras):
    print photo.get('title')