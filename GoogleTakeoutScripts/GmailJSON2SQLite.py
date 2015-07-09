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

with open("constants.yaml", 'r') as ymlfile:
    constants = yaml.load(ymlfile)

DATABASE_NAME = constants['database']
DATABASE_LOC = constants['path']

database = SqliteDatabase(constants['databaseLoc'], threadlocals=True)
database.connect()

#with open(Gmail2JSON.OUT_FILE, 'r'):
    #TODO Get into database
