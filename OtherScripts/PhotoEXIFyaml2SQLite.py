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
import yaml
import peewee
from databaseSetup import Photos
from glob import glob


# Lists holding the dictionaries that will be bulk inserted into the database
jpg_queries = []
raw_queries = []

def jpg_exif_parser(yaml_exif):
    name = yaml_exif.get('Filename')
    date = yaml_exif.get('Image DateTime')
    iso = yaml_exif.get('EXIF ISOSpeedRatings')
    camera_model = yaml_exif.get('Image Model')
    shutter = yaml_exif.get('EXIF ShutterSpeedValue')
    exposure = yaml_exif.get('EXIF ExposureTime')
    apeture = yaml_exif.get('EXIF ApertureValue')
    flash = yaml_exif.get('EXIF Flash')

    jpg_queries.append({'name': name, 'date': date, 'location': None,
                        'shutter': '', 'iso': iso, 'aperture': '',
                        'manufacturer': '', 'camera_model': camera_model, 'exposure_priority': '', 'exposure_mode': '', 'flash': '',
                        'lens_model': '', 'focal_length': '', 'service': None, 'date_uploaded': None, 'url': None})

with open(os.path.join("..","constants.yaml"), 'r') as ymlfile:
    constants = yaml.load(ymlfile)

###################################################################
#
#             Start of .JPG YAML Processing
#
###################################################################
photos = [y for x in os.walk(constants.get('outputDir')) for y in glob(os.path.join(x[0], 'photo.exif.*.*.yml'))]

for photo in photos:
    exif_data = yaml.load(photo)
    jpg_exif_parser(exif_data)