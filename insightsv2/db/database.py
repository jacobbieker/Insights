
import os
import datetime
import peewee
import yaml
from playhouse.migrate import *
import phonenumbers
from playhouse.pool import PooledSqliteExtDatabase
from playhouse.sqliteq import SqliteQueueDatabase

class BaseModel(Model):
    class Meta:
        database = db

class InsightsDatabase(object):

    def __init__(self, config):

        if type(config) is dict:
            self.config = config
        elif type(config) is str:
            with open(config, 'r') as ymlfile:
                self.config = yaml.load(ymlfile)

        # Create database and connect to it
        self.db = SqliteQueueDatabase(self.config['name'])