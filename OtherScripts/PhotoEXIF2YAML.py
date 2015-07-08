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

#TODO Add support for multiple locations
#TODO Check for filename conflicts and rename if necessary
locations = 'C:\Users\jacob_000\OneDrive\EOS Pictures'

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
            with open(os.path.join('C:\Development\Insights\output', 'photo.exif.' + file_name[0] + file_name[1]  + '.yml'),
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
            with open(os.path.join('C:\Development\Insights\output', 'photo.exif.' + file_name[0] + file_name[1]  + '.yml'),
                      'w') as yaml_output:
                yaml_output.write("%s: %s" % ('Filename', file_name[0]))
                for tag in raw_output._fields:
                    print tag
    ###################################################################
    #
    #             end of .CR2 Processing
    #
    ###################################################################