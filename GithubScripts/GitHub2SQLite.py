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
        code = input('Enter 2FA code: ')
    return code

# Not ideal, but gets it done for now
password = ''
while not password:
    password = input('Password for GitHub: ')

# Authentication
# Have to do this because when the command is called from the import in any subfolder it cannot find the dbconfig
if __name__ == "__main__":
    with open(os.path.join("..","access.yaml"), 'r') as access:
        access_config = yaml.load(access)
else:
    with open(os.path.join("access.yaml"), 'r') as access:
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
