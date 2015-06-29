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
