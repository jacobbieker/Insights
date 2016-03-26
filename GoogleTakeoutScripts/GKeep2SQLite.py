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
__author__ = 'Jacob Bieker'
import os
import yaml
from peewee import *
from databaseSetup import Document
from glob import glob
from bs4 import BeautifulSoup
from datetime import datetime

# Have to do this because when the command is called from the import in any subfolder it cannot find the dbconfig
if __name__ == "__main__":
    with open(os.path.join("constants.yaml"), 'r') as ymlfile:
        constants = yaml.load(ymlfile)
else:
    with open("constants.yaml", 'r') as ymlfile:
        constants = yaml.load(ymlfile)

rootdir = os.path.join(constants.get("dataDir"), "Takeout", "Keep")
keep_data = [y for x in os.walk(rootdir) for y in glob(os.path.join(x[0], '*.html'))]

for keep_file in keep_data:
    with open(os.path.join(rootdir, keep_file), "r") as source:
        html_file = BeautifulSoup(source.read(), "lxml")
        # Content should be the body text
        content = html_file.find("div", {"class": "content"})
        # Title is the name of the note
        title = html_file.find("div", {"class": "title"})
        # Heading has the time of the note
        date = html_file.find("div", {"class": "heading"})
        if date is not None:
            if title is not None:
                if content is not None:
                    Document.insert({"date": date.text,
                                     "type": "note",
                                     "application": "Google Keep",
                                     "content": content.text,
                                     "title": title.text}).execute()
                else:
                    Document.insert({"date": date.text,
                                     "type": "note",
                                     "application": "Google Keep",
                                     "title": title.text}).execute()
            elif content is not None:
                Document.insert({"date": date.text,
                                 "type": "note",
                                 "content": content.text,
                                 "application": "Google Keep"}).execute()
            else:
                Document.insert({"date": date.text,
                                 "type": "note",
                                 "application": "Google Keep"}).execute()