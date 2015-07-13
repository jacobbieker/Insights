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
import os
import yaml
import flickrapi
import json
import webbrowser
import insights

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