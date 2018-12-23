import os
import peewee
import multiprocessing


class BaseConvertor(object):

    def __init__(self, database='insights.db'):
        self.database = database

    def convert_to_json(self, paths, use_multiprocessing=False):
        return NotImplementedError

    def convert_to_db(self, paths, use_multiprocessing=False):
        return NotImplementedError

    def connect_to_service(self):
        return NotImplementedError
