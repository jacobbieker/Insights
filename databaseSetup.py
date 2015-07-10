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
import os
import datetime
import peewee
import yaml
from playhouse.migrate import *
#Define the fields used in the database so migrate can be called and used:
date_field = DateField(null=True)
time_field = TimeField(null=True)
datetime_field = DateTimeField(null=True)
char_field = CharField(null=True)
text_field = TextField(null=True)
int_field = IntegerField(null=True)
double_field = DoubleField(null=True)
boolean_field = BooleanField(null=True)
timestamp_field = DateTimeField(default=datetime.datetime.now)

#Create base database
class BaseModel(peewee.Model):
    class Meta:
        database = database

'''
Since there does not seem to be a way to create tables programmatically using peewee, we'll create all the tables in
config, and then add a column using the database migration tools programmically. Limitation: have to create atleast one
column per table by default
'''

class Message(BaseModel):
    type = text_field
    date = datetime_field
    time = time_field
    sender = char_field
    reciever = char_field
    message = text_field
    length = int_field
    timestamp = timestamp_field

class Word(BaseModel):
    word = char_field
    length = int_field
    occurences = int_field
    timestamp = timestamp_field

class Call(BaseModel):
    date = datetime_field
    time = time_field
    caller = char_field
    reciever = char_field
    length = double_field
    answered = boolean_field
    timestamp = timestamp_field

class Voicemail(BaseModel):
    date = datetime_field
    time = time_field
    caller = char_field
    message = text_field
    timestamp = timestamp_field

class Contacts(BaseModel):
    name = char_field
    first_contact = datetime_field
    last_contact = datetime_field
    last_message = text_field
    phone_numbers = int_field
    country_code = text_field
    last_number = int_field
    timestamp = timestamp_field

class Locations(BaseModel):
    date = datetime_field
    time = time_field
    longitude = double_field
    latitude = double_field
    continent = char_field
    country = char_field
    state = char_field
    zip = int_field
    city = char_field
    street = text_field
    name = text_field
    timestamp = timestamp_field

class Jobs(BaseModel):
    title = char_field
    company = char_field
    description = text_field
    start_date = datetime_field
    end_date = datetime_field
    type = text_field
    currently_working = boolean_field
    location = text_field
    timestamp = timestamp_field

class SocialMedia(BaseModel):
    type = char_field
    date = datetime_field
    time = time_field
    message = text_field
    tags = text_field
    urls = text_field
    timestamp = timestamp_field

class Photos(BaseModel):
    name = char_field
    date = datetime_field
    time = time_field
    location = text_field
    shutter = text_field
    iso = int_field
    shot_format = text_field
    aperture = text_field
    manufacturer = char_field
    camera_model = char_field
    exposure_priority = text_field
    exposure_mode = text_field
    flash = boolean_field
    lens_model = text_field
    focal_length = double_field
    service = text_field
    date_uploaded = datetime_field
    timestamp = timestamp_field

class Calendars(BaseModel):
    start_date = datetime_field
    start_time = time_field
    end_date = datetime_field
    end_time = time_field
    type = char_field
    which_calender = char_field
    description = text_field
    name = text_field
    duration = double_field
    is_task = boolean_field
    timestamp = timestamp_field

if __name__ == "__main__":
    with open("dbconfig.yaml", 'r') as ymlfile:
        config = yaml.load(ymlfile)

    DB_NAME = config.get('sqlite').get('name') + '.db'
    #remove old database if in the current directory
    if os.path.isfile(DB_NAME):
        database = SqliteDatabase(DB_NAME)
        database.connect()
    else:
        #Check to see what type of database wanted, and creates the type specificed
        if config.get('sqlite').get('type') == 'extended':
            from playhouse.sqlite_ext import SqliteExtDatabase
            database = SqliteExtDatabase(DB_NAME, threadlocals=True)
        elif config.get('sqlite').get('type') == 'apsw':
            from playhouse.apsw_ext import APSWDatabase
            database = APSWDatabase(DB_NAME, threadlocals=True)
        else:
            database = SqliteDatabase(DB_NAME, threadlocals=True)

        database.connect()

        def create_tables():
            Calendars.create_table()
            Message.create_table()
            Locations.create_table()
            Call.create_table()
            Voicemail.create_table()
            Word.create_table()
            Jobs.create_table()
            Contacts.create_table()
            SocialMedia.create_table()
            Photos.create_table()

        create_tables()