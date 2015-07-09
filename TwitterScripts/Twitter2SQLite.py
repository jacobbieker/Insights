__author__ = 'Jacob'
'''
Unlike Takeout scripts, this deals with live data, as there is no known download-your-data from Twitter
'''
import os
from peewee import *
import tweepy
import json
import yaml

#Authentication with Twitter
with open("access.yaml", 'r') as access:
    access_config = yaml.load(access)


auth = tweepy.OAuthHandler(access_config['twitter']['key'], access_config['twitter']['secret'])

#Redirect user to authenticate with Twitter before continuing
try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print 'Error! Failed to get request token.'

# Example w/o callback (desktop)
verifier = raw_input('Verifier:').strip()

# Try to get access token for use later
try:
    auth.get_access_token(verifier=verifier)
except:
    print 'Error! Could not get access token'

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
    print friend

# Iterate through the first 200 statuses in the friends timeline
for status in tweepy.Cursor(api.friends_timeline).items(200):
    # Process the status here
    print status

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