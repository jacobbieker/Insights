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
import phonenumbers

if __name__ == "__main__":
    with open("dbconfig.yaml", 'r') as ymlfile:
        config = yaml.load(ymlfile)

    DB_NAME = config.get('sqlite').get('name') + '.db'
    # remove old database if in the current directory
    if os.path.isfile(DB_NAME):
        database = SqliteDatabase(DB_NAME)
        database.connect()
    else:
        # Check to see what type of database wanted, and creates the type specificed
        if config.get('sqlite').get('type') == 'extended':
            from playhouse.sqlite_ext import SqliteExtDatabase

            database = SqliteExtDatabase(DB_NAME, threadlocals=True)
        elif config.get('sqlite').get('type') == 'apsw':
            from playhouse.apsw_ext import APSWDatabase

            database = APSWDatabase(DB_NAME, threadlocals=True)
        else:
            database = SqliteDatabase(DB_NAME, threadlocals=True)

    database.connect()


    # Create base database
    class BaseModel(peewee.Model):
        class Meta:
            database = database


    class Contacts(BaseModel):
        name = CharField(null=True)
        birthday = DateField(null=True)
        address = TextField(null=True)
        email_1 = TextField(null=True)
        email_2 = TextField(null=True)
        email_3 = TextField(null=True)
        email_4 = TextField(null=True)
        first_contact = DateTimeField(null=True)
        last_contact = DateTimeField(null=True)
        last_message = TextField(null=True)
        phone_number_1 = TextField(null=True)
        phone_number_2 = TextField(null=True)
        phone_number_3 = TextField(null=True)
        phone_number_4 = TextField(null=True)
        country_code = TextField(null=True)
        last_number = TextField(null=True)
        url = TextField(null=True)
        timestamp = DateTimeField(default=datetime.datetime.now())


    class Message(BaseModel):
        type = TextField(null=True)
        date = DateTimeField(null=True)
        time = TimeField(null=True)
        sender = CharField(null=True)
        reciever = CharField(null=True)
        message = TextField(null=True)
        length = IntegerField(null=True)
        contact = ForeignKeyField(Contacts, null=True)
        timestamp = DateTimeField(default=datetime.datetime.now())


    class Word(BaseModel):
        word = CharField(null=True)
        length = IntegerField(null=True)
        occurences = IntegerField(null=True)
        timestamp = DateTimeField(default=datetime.datetime.now())


    class Call(BaseModel):
        date = DateTimeField(null=True)
        time = TimeField(null=True)
        caller = CharField(null=True)
        reciever = CharField(null=True)
        length = TimeField(null=True)
        answered = TextField(null=True)
        contact = ForeignKeyField(Contacts, null=True)
        timestamp = DateTimeField(default=datetime.datetime.now())


    class Voicemail(BaseModel):
        date = DateTimeField(null=True)
        time = TimeField(null=True)
        caller = CharField(null=True)
        message = TextField(null=True)
        contact = ForeignKeyField(Contacts, null=True)
        timestamp = DateTimeField(default=datetime.datetime.now())


    class Locations(BaseModel):
        date = DateTimeField(null=True)
        time = TimeField(null=True)
        longitude = DoubleField(null=True)
        latitude = DoubleField(null=True)
        continent = CharField(null=True)
        country = CharField(null=True)
        state = CharField(null=True)
        zip = TextField(null=True)
        city = CharField(null=True)
        area = TextField(null=True)
        county = TextField(null=True)
        street = TextField(null=True)
        name = TextField(null=True)
        provider = CharField(null=True)
        bound_north = DoubleField(null=True)
        bound_south = DoubleField(null=True)
        bound_east = DoubleField(null=True)
        bound_west = DoubleField(null=True)
        timestamp = DateTimeField(default=datetime.datetime.now())


    class Jobs(BaseModel):
        title = CharField(null=True)
        company = CharField(null=True)
        description = TextField(null=True)
        start_date = DateTimeField(null=True)
        end_date = DateTimeField(null=True)
        type = TextField(null=True)
        currently_working = BooleanField()
        location = TextField(null=True)
        timestamp = DateTimeField(default=datetime.datetime.now())


    class SocialMedia(BaseModel):
        type = CharField(null=True)
        date = DateTimeField(null=True)
        time = TimeField(null=True)
        message = TextField(null=True)
        tags = TextField(null=True)
        urls = TextField(null=True)
        timestamp = DateTimeField(default=datetime.datetime.now())


    class Photos(BaseModel):
        name = CharField(null=True)
        date = DateTimeField(null=True)
        time = TimeField(null=True)
        location = TextField(null=True)
        shutter = TextField(null=True)
        iso = IntegerField(null=True)
        shot_format = TextField(null=True)
        aperture = TextField(null=True)
        manufacturer = CharField(null=True)
        camera_model = CharField(null=True)
        exposure_priority = TextField(null=True)
        exposure_mode = TextField(null=True)
        flash = BooleanField()
        lens_model = TextField(null=True)
        focal_length = DoubleField(null=True)
        service = TextField(null=True)
        date_uploaded = DateTimeField(null=True)
        url = TextField(null=True)
        timestamp = DateTimeField(default=datetime.datetime.now())


    class Calendars(BaseModel):
        start_date = DateTimeField(null=True)
        start_time = TimeField(null=True)
        end_date = DateTimeField(null=True)
        end_time = TimeField(null=True)
        type = CharField(null=True)
        which_calender = CharField(null=True)
        description = TextField(null=True)
        location = TextField(null=True)
        name = TextField(null=True)
        duration = DoubleField(null=True)
        is_task = BooleanField()
        timestamp = DateTimeField(default=datetime.datetime.now())


    class Sleep(BaseModel):
        start_time = DateTimeField(null=True)
        end_time = DateTimeField(null=True)
        location = ForeignKeyField(Locations, null=True)
        duration = DoubleField(null=True)
        application = CharField(null=True)
        cycles = IntegerField(null=True)
        rating = DoubleField(null=True)
        comments = TextField(null=True)
        deep_sleep = FloatField(null=True)
        noise = FloatField(null=True)


    class Activity(BaseModel):
        date = DateField(null=True)
        start_time = TimeField(null=True)
        end_time = TimeField(null=True)
        location = ForeignKeyField(Locations, null=True)
        duration = DoubleField(null=True)
        application = CharField(null=True)
        rating = DoubleField(null=True)
        comments = TextField(null=True)
        type = CharField(null=True)
        calories = DoubleField(null=True)
        avg_altitude = DoubleField(null=True)
        max_altitude = DoubleField(null=True)
        min_altitude = DoubleField(null=True)


    class Heart(BaseModel):
        start_time = TimeField(null=True)
        end_time = TimeField(null=True)
        location = ForeignKeyField(Locations, null=True)
        duration = DoubleField(null=True)
        application = CharField(null=True)
        lowest = DoubleField(null=True)
        average = DoubleField(null=True)
        highest = DoubleField(null=True)
        activity = ForeignKeyField(Activity, null=True)


    Calendars.create_table(True)
    Message.create_table(True)
    Locations.create_table(True)
    Call.create_table(True)
    Voicemail.create_table(True)
    Word.create_table(True)
    Jobs.create_table(True)
    Contacts.create_table(True)
    SocialMedia.create_table(True)
    Photos.create_table(True)
    Sleep.create_table(True)
    Activity.create_table(True)
    Heart.create_table(True)

    database.close()
# Have to do this because when the command is called from the import in any subfolder it cannot find the dbconfig
if __name__ != "__main__":
    print(__name__)
    if __name__ == "databaseSetup":
        with open("constants.yaml", 'r') as ymlfile:
            config = yaml.load(ymlfile)
    else:
        with open(os.path.join("..", "constants.yaml"), 'r') as ymlfile:
            config = yaml.load(ymlfile)
else:
    with open("constants.yaml", 'r') as ymlfile:
        config = yaml.load(ymlfile)

'''
As of right now, this should create a database in each folder the script is run, to then combine them later
Peewee seems to have a problem with connecting to a database that is not in the current folder
'''


# Create base database
class BaseModel(peewee.Model):
    class Meta:
        database = SqliteDatabase(config.get('databaseLoc'))


class Contacts(BaseModel):
    name = CharField(null=True)
    birthday = DateField(null=True)
    address = TextField(null=True)
    email_1 = TextField(null=True)
    email_2 = TextField(null=True)
    email_3 = TextField(null=True)
    email_4 = TextField(null=True)
    first_contact = DateTimeField(null=True)
    last_contact = DateTimeField(null=True)
    last_message = TextField(null=True)
    phone_number_1 = TextField(null=True)
    phone_number_2 = TextField(null=True)
    phone_number_3 = TextField(null=True)
    phone_number_4 = TextField(null=True)
    country_code = TextField(null=True)
    last_number = IntegerField(null=True)
    url = TextField(null=True)
    timestamp = DateTimeField(default=datetime.datetime.now())


class Message(BaseModel):
    type = TextField(null=True)
    date = DateTimeField(null=True)
    time = TimeField(null=True)
    sender = CharField(null=True)
    reciever = CharField(null=True)
    message = TextField(null=True)
    length = IntegerField(null=True)
    contact = ForeignKeyField(Contacts, null=True)
    timestamp = DateTimeField(default=datetime.datetime.now())


class Word(BaseModel):
    word = CharField(null=True)
    length = IntegerField(null=True)
    occurences = IntegerField(null=True)
    timestamp = DateTimeField(default=datetime.datetime.now())


class Call(BaseModel):
    date = DateTimeField(null=True)
    time = TimeField(null=True)
    caller = CharField(null=True)
    reciever = CharField(null=True)
    length = TimeField(null=True)
    answered = TextField(null=True)
    contact = ForeignKeyField(Contacts, null=True)
    timestamp = DateTimeField(default=datetime.datetime.now())


class Voicemail(BaseModel):
    date = DateTimeField(null=True)
    time = TimeField(null=True)
    caller = CharField(null=True)
    message = TextField(null=True)
    contact = ForeignKeyField(Contacts, null=True)
    timestamp = DateTimeField(default=datetime.datetime.now())


class Locations(BaseModel):
    date = DateTimeField(null=True)
    time = TimeField(null=True)
    longitude = DoubleField(null=True)
    latitude = DoubleField(null=True)
    continent = CharField(null=True)
    country = CharField(null=True)
    state = CharField(null=True)
    zip = TextField(null=True)
    city = CharField(null=True)
    area = TextField(null=True)
    county = TextField(null=True)
    street = TextField(null=True)
    name = TextField(null=True)
    provider = CharField(null=True)
    bound_north = DoubleField(null=True)
    bound_south = DoubleField(null=True)
    bound_east = DoubleField(null=True)
    bound_west = DoubleField(null=True)
    timestamp = DateTimeField(default=datetime.datetime.now())


class Jobs(BaseModel):
    title = CharField(null=True)
    company = CharField(null=True)
    description = TextField(null=True)
    start_date = DateTimeField(null=True)
    end_date = DateTimeField(null=True)
    type = TextField(null=True)
    currently_working = BooleanField()
    location = TextField(null=True)
    timestamp = DateTimeField(default=datetime.datetime.now())


class SocialMedia(BaseModel):
    type = CharField(null=True)
    date = DateTimeField(null=True)
    time = TimeField(null=True)
    message = TextField(null=True)
    tags = TextField(null=True)
    urls = TextField(null=True)
    timestamp = DateTimeField(default=datetime.datetime.now())


class Photos(BaseModel):
    name = CharField(null=True)
    date = DateTimeField(null=True)
    time = TimeField(null=True)
    location = TextField(null=True)
    shutter = TextField(null=True)
    iso = IntegerField(null=True)
    shot_format = TextField(null=True)
    aperture = TextField(null=True)
    manufacturer = CharField(null=True)
    camera_model = CharField(null=True)
    exposure_priority = TextField(null=True)
    exposure_mode = TextField(null=True)
    flash = BooleanField()
    lens_model = TextField(null=True)
    focal_length = DoubleField(null=True)
    service = TextField(null=True)
    date_uploaded = DateTimeField(null=True)
    timestamp = DateTimeField(default=datetime.datetime.now())


class Calendars(BaseModel):
    start_date = DateTimeField(null=True)
    start_time = TimeField(null=True)
    end_date = DateTimeField(null=True)
    end_time = TimeField(null=True)
    type = CharField(null=True)
    which_calender = CharField(null=True)
    description = TextField(null=True)
    name = TextField(null=True)
    location = TextField(null=True)
    duration = DoubleField(null=True)
    is_task = BooleanField()
    timestamp = DateTimeField(default=datetime.datetime.now())


class Sleep(BaseModel):
    start_time = DateTimeField(null=True)
    end_time = DateTimeField(null=True)
    location = ForeignKeyField(Locations, null=True)
    duration = DoubleField(null=True)
    application = CharField(null=True)
    cycles = IntegerField(null=True)
    rating = DoubleField(null=True)
    comments = TextField(null=True)
    deep_sleep = FloatField(null=True)
    noise = FloatField(null=True)


class Activity(BaseModel):
    date = DateField(null=True)
    start_time = TimeField(null=True)
    end_time = TimeField(null=True)
    location = ForeignKeyField(Locations, null=True)
    duration = DoubleField(null=True)
    application = CharField(null=True)
    rating = DoubleField(null=True)
    comments = TextField(null=True)
    type = CharField(null=True)
    calories = DoubleField(null=True)
    avg_altitude = DoubleField(null=True)
    max_altitude = DoubleField(null=True)
    min_altitude = DoubleField(null=True)


class Heart(BaseModel):
    start_time = TimeField(null=True)
    end_time = TimeField(null=True)
    location = ForeignKeyField(Locations, null=True)
    duration = DoubleField(null=True)
    application = CharField(null=True)
    lowest = DoubleField(null=True)
    average = DoubleField(null=True)
    highest = DoubleField(null=True)
    activity = ForeignKeyField(Activity, null=True)


'''
Set of functions to normalize data and standardize different inputs and queries
'''


def get_contact_by_number(phone_number):
    try_1 = Contacts.get(phone_number_1=phone_number)
    try_2 = Contacts.get(phone_number_2=phone_number)
    try_3 = Contacts.get(phone_number_3=phone_number)
    try_4 = Contacts.get(phone_number_4=phone_number)
    if try_1 is not None:
        return try_1
    elif try_2 is not None:
        return try_2
    elif try_3 is not None:
        return try_3
    elif try_4 is not None:
        return try_4
    else:
        print("Contact does not exist")
        return None


def get_contact_by_email(email):
    try_1 = Contacts.get(email_1=email)
    try_2 = Contacts.get(email_2=email)
    try_3 = Contacts.get(email_3=email)
    try_4 = Contacts.get(email_4=email)
    if try_1 is not None:
        return try_1
    elif try_2 is not None:
        return try_2
    elif try_3 is not None:
        return try_3
    elif try_4 is not None:
        return try_4
    else:
        print("Contact does not exist")
        return None


def normalize_number(phone_number):
    parsed = phonenumbers.parse(phone_number, 'US')
    normalized = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    return normalized
    # Make all phone numbers the same setup
