__author__ = 'Jacob Bieker'
from github3 import *
import github3
import os
import peewee
import yaml

# Functions for use later
def my_two_factor_function():
    code = ''
    while not code:
        # The user could accidentally press Enter before being ready,
        # let's protect them from doing that.
        code = raw_input('Enter 2FA code: ')
    return code

# Not ideal, but gets it done for now
password = ''
while not password:
    password = raw_input('Password for GitHub: ')

# Authentication
with open("access.yaml", 'r') as access:
    access_config = yaml.load(access)

username = access_config.get('github').get('username')

if access_config.get('github').get('twoFactor'):
    login_user = github3.login(username=username, password=password,
                               two_factor_callback=my_two_factor_function)
else:
    login_user = github3.login(username=username, password=password)

# Saves token and ID for later use
with open("access.yaml", 'w') as access:
    access_config.get('github').get('token').set(login_user.token)
    access_config.get('github').get('authID').set(login_user.id)
    access.write(yaml.dump(access_config, default_flow_style=False))
