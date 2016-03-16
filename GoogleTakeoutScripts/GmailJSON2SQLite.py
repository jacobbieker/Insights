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
from peewee import *
import yaml
import os

# Have to do this because when the command is called from the import in any subfolder it cannot find the dbconfig
if __name__ != "__main__":
    with open(os.path.join("..", "constants.yaml"), 'r') as ymlfile:
        constants = yaml.load(ymlfile)
else:
    with open("constants.yaml", 'r') as ymlfile:
        constants = yaml.load(ymlfile)

DATABASE_NAME = constants.get('database')
DATABASE_LOC = constants.get('path')

database = SqliteDatabase(constants.get('databaseLoc'), threadlocals=True)
database.connect()

#with open(Gmail2JSON.OUT_FILE, 'r'):
    #TODO Get into database

