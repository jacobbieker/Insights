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
'''
Unlike Takeout scripts, this deals with live data, as there is no known download-your-data from Twitter
'''
import tweepy

# Authentication with Twitter
from insights.io import config

if __name__ != "__main__":
    configuration_files = config.import_yaml_files(".", ["access.yaml"])
    access_config = configuration_files[0]
else:
    configuration_files = config.import_yaml_files("..", ["access.yaml"])
    access_config = configuration_files[0]


auth = tweepy.OAuthHandler(access_config.get('twitter').get('key'), access_config.get('twitter').get('secret'))

#Redirect user to authenticate with Twitter before continuing
try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print('Error! Failed to get request token.')

# Example w/o callback (desktop)
verifier = input('Verifier:').strip()

# Try to get access token for use later
try:
    auth.get_access_token(verifier=verifier)
except:
    print('Error! Could not get access token')

#Token and secret
#TODO save to access_config.yaml to read later and skip above steps
token = auth.access_token
secret = auth.access_token_secret

#Start API access
api = tweepy.API(auth)


###################################################################
#
#             Start of Twitter Friends Processing
#
###################################################################

# Iterate through all of the authenticated user's friends
for friend in tweepy.Cursor(api.friends).items():
    #Process the friend here
    print(friend)

# Iterate through the first 200 statuses in the friends timeline
for status in tweepy.Cursor(api.friends_timeline).items(200):
    # Process the status here
    print(status)

###################################################################
#
#             End of Twitter Friends Processing
#
###################################################################
###################################################################
#
#             Start of Trends Processing
#
###################################################################
oregon_whoeid = 2347596
us_whoeid = 	23424977
word_whoeid = 1

#Get trends for each of those and save to file
###################################################################
#
#             End of Trends Processing
#
###################################################################