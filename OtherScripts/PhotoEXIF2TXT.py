__author__ = 'Jacob Bieker'
import exifread
from exifread import *
import os
import json
import yaml
from glob import glob


location = 'C:\Users\jacob_000\OneDrive\EOS Pictures'

photos = [y for x in os.walk(location) for y in glob(os.path.join(x[0], '*.JPG'))]

for photo in photos:
    file_name = os.path.splitext(os.path.basename(photo))
    with open(photo, 'rb') as image:
        #Return EXIF tags
        metadata = exifread.process_file(image)
        with open(os.path.join('C:\Development\Insights\output', 'picture.exif.' + file_name[0]  + '.txt'), 'w') as json_output:
            for tag in metadata.keys():
                if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'EXIF MakerNote'):
                    json_output.write("\n%s: %s" % (tag, metadata[tag]))
            #json_array = json.dump(metadata, json_output, sort_keys=True, indent=4)