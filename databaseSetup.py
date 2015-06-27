__author__ = 'Jacob'
from peewee import *
import sqlite3
import os
from os.path import basename
import yaml

with open("dbconfig.yaml", 'r') as ymlfile:
    config = yaml.load(ymlfile)

#remove old database if in the current directory
os.remove("ownData.db")

database = SqliteDatabase(config['sqlite']['name'] + ".db", threadlocals=True)
database.connect()

class BaseModel(Model):
    class Meta:
        database = database

for table in config['sqlite']['tables']:
    print(table)


class Text(BaseModel):
    date = DateField(null=True)
    time = TimeField(null=True)
    sender = CharField(null=True)
    receiver = CharField(null=True)
    message = TextField(null=True)
    length = IntegerField(null=True)



class Contact(BaseModel):
    name = CharField(null=True)
    avgLength = DoubleField(null=True)
    firstContact = DateField(null=True)
    lastContact = DateField(null=True)


class Word(BaseModel):
    word = CharField(null=True)
    length = IntegerField(null=True)
    occurrences = IntegerField(null=True)


class Call(BaseModel):
    date = DateField(null=True)
    time = TimeField(null=True)
    caller = CharField(null=True)
    receiver = CharField(null=True)
    length = DoubleField(null=True)

class Voicemail(BaseModel):
    date = DateField(null=True)
    time = TimeField(null=True)
    caller = CharField(null=True)
    message = TextField(null=True)


def create_tables():
    Contact.create_table()
    Text.create_table()
    Call.create_table()
    Voicemail.create_table()
    Word.create_table()

create_tables()
