__author__ = 'Jacob Bieker'
from github3 import *
import github3
import os
import peewee
import yaml

def my_two_factor_function():
    code = ''
    while not code:
        # The user could accidentally press Enter before being ready,
        # let's protect them from doing that.
        code = raw_input('Enter 2FA code: ')
    return code

#Authentication with Instagram
with open("access.yaml", 'r') as access:
    access_config = yaml.load(access)

username = access_config['github']['username']

if access_config['github']['twoFactor']:
    auth = github3.login(username=username, password=password,
                  two_factor_callback=my_two_factor_function)
else:
    auth = github3.login(username=username, password=password)