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
import exifread
from exifread import *
import os
import json
import yaml
from glob import glob
from rawkit.raw import Raw
from rawkit.metadata import Metadata
import libraw

#TODO Check for filename conflicts and rename if necessary

with open(os.path.join("..","access.yaml"), 'r') as access:
    access_config = yaml.load(access)
locations = access_config.get('local').get('photoLocations')
with open(os.path.join("..","constants.yaml"), 'r') as ymlfile:
    constants = yaml.load(ymlfile)
#Go through each location:
for location in locations:
    ###################################################################
    #
    #             Start of .JPG Processing
    #
    ###################################################################
    photos = [y for x in os.walk(location) for y in glob(os.path.join(x[0], '*.JPG'))]

    for photo in photos:
        file_name = os.path.splitext(os.path.basename(photo))
        with open(photo, 'rb') as image:
            #Return EXIF tags
            metadata = exifread.process_file(image)
            with open(os.path.join(constants.get('outputDir'), 'photo.exif.' + file_name[0] + file_name[1]  + '.yml'),
                      'w') as yaml_output:
                yaml_output.write("%s: %s" % ('Filename', file_name[0]))
                for tag in metadata.keys():
                    if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'EXIF MakerNote'):
                        yaml_output.write("\n%s: %s" % (tag, metadata[tag]))
    ###################################################################
    #
    #             End of .JPG Processing
    #
    ###################################################################
    ###################################################################
    #
    #             Start of .CR2 Processing
    #
    ###################################################################
    canon_raws = [y for x in os.walk(location) for y in glob(os.path.join(x[0], '*.CR2'))]

    for raw_file in canon_raws:
        file_name = os.path.splitext(os.path.basename(raw_file))
        with Raw(filename=raw_file) as raw:
            raw_output = Metadata
            with open(os.path.join(constants.get('outputDir'), 'photo.exif.' + file_name[0] + file_name[1]  + '.yml'),
                      'w') as yaml_output:
                yaml_output.write("%s: %s" % ('Filename', file_name[0]))
                for tag in raw_output._fields:
                    print(tag)
    ###################################################################
    #
    #             end of .CR2 Processing
    #
    ###################################################################