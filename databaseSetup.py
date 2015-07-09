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
from peewee import *
import yaml
from playhouse.migrate import *

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

    #Define the fields used in the database so migrate can be called and used:
    date_field = DateField(null=True)
    time_field = TimeField(null=True)
    datetime_field = DateTimeField(null=True)
    char_field = CharField(null=True)
    text_field = TextField(null=True)
    int_field = IntegerField(null=True)
    double_field = DoubleField(null=True)
    boolean_field = BooleanField(null=True)

    #Create base database
    class BaseModel(Model):
        class Meta:
            database = database

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

    class SocialMedia(BaseModel):
        default = datetime_field

    class Photos(BaseModel):
        default = datetime_field

    def create_tables():
        Message.create_table()
        Locations.create_table()
        Call.create_table()
        Voicemail.create_table()
        Word.create_table()
        Jobs.create_table()
        Contacts.create_table()
        SocialMedia.create_table()
        Photos.create_table()

    #TODO Check if certain tables exist and do not create them if they do
    create_tables()

    '''
    Now programmatically add columns to the tables
    '''
    migrator = SqliteMigrator(database)

    for table in config.get('sqlite').get('tables'):
        for column in config.get('sqlite').get('tables').get(table):
            print column.keys()
            #Use mcol_namator to add a column for each field
            col_name = column.keys()[0]
            col_type = column.values()[0]
            if col_type == 'string':
                migrate(
                    migrator.add_column(table, col_name, text_field)
                )
            elif col_type == 'char':
                migrate(
                    migrator.add_column(table, col_name, char_field)
                )
            elif col_type == 'date':
                migrate(
                    migrator.add_column(table, col_name, datetime_field)
                )
            elif col_type == 'time':
                migrate(
                    migrator.add_column(table, col_name, time_field)
                )
            elif col_type == 'int':
                migrate(
                    migrator.add_column(table, col_name, int_field)
                )
            elif col_type == 'double':
                migrate(
                    migrator.add_column(table, col_name, double_field)
                )
            elif col_type == 'boolean':
                migrate(
                    migrator.add_column(table, col_name, boolean_field)
                )
        #Now delete the default table
        migrate(
            migrator.drop_column(table, 'default')
        )
