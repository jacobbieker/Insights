__author__ = 'Jacob'
import os
from peewee import *
import yaml
from playhouse.migrate import *

with open("dbconfig.yaml", 'r') as ymlfile:
    config = yaml.load(ymlfile)

#remove old database if in the current directory
os.remove(config['sqlite']['name'] + ".db")

database = SqliteDatabase(config['sqlite']['name'] + ".db", threadlocals=True)
database.connect()

#Define the fields used in the database so migrate can be called and used:
date_field = DateField(null=True)
time_field = TimeField(null=True)
datetime_field = DateTimeField(null=True)
char_field = CharField(null=True)
text_field = TextField(null=True)
int_field = IntegerField(null=True)
double_field = DoubleField(null=True)

#Create base database
class BaseModel(Model):
    class Meta:
        database = database

for table in config['sqlite']['tables']:
    print(table)

'''
Since there does not seem to be a way to create tables programmatically using peewee, we'll create all the tables in
config, and then add a column using the database migration tools programmically. Limitation: have to create atleast one
column per table by default
'''

class Message(BaseModel):
    default = datetime_field

class Word(BaseModel):
    default = datetime_field

class Call(BaseModel):
    default = datetime_field

class Voicemail(BaseModel):
    default = datetime_field

class Contacts(BaseModel):
    default = datetime_field

class Locations(BaseModel):
    default = datetime_field

class Jobs(BaseModel):
    default = datetime_field

def create_tables():
    Message.create_table()
    Locations.create_table()
    Call.create_table()
    Voicemail.create_table()
    Word.create_table()
    Jobs.create_table()
    Contacts.create_table()

create_tables()

'''
Now programmatically add columns to the tables
'''
migrator = SqliteMigrator(database)

for table in config['sqlite']['tables']:
    for column in table:
        print column