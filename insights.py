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
'''
This file unzips downloaded files, gets data, and sets up file structure for use by the rest of the scripts
'''
__author__ = 'Jacob Bieker'
import os
import glob
import zipfile
import yaml

# read config data on database
with open("dbconfig.yaml", 'r') as ymlfile:
    config = yaml.load(ymlfile)
with open("access.yaml", 'r') as access:
    access_config = yaml.load(access)

# Constant current directory used by rest of the scripts:
PATH = os.path.abspath("./")
OUT_PATH = os.path.join(PATH, "output")
DATA_PATH = os.path.join(PATH, "data")
DB_NAME = config.get('sqlite').get('name') + '.db'
GOOGLE_SCRIPTS = os.path.join(PATH, "GoogleTakeoutScripts")
FACEBOOK_SCRIPTS = os.path.join(PATH, "FacebookScripts")
TWITTER_SCRIPTS = os.path.join(PATH, "TwitterScripts")
INSTAGRAM_SCRIPTS = os.path.join(PATH, "InstagramScripts")
OTHER_SCRIPTS = os.path.join(PATH, "OtherScripts")
BIOMETRIC_SCRIPTS = os.path.join(PATH, "BiometricScripts")

# Create config.yaml to be used for other scripts, so that they don't import insights.py
constants = {
    'path': PATH,
    'dataDir': DATA_PATH,
    'outputDir': OUT_PATH,
    'database': DB_NAME,
    'databaseLoc': os.path.join(PATH, DB_NAME),
    'googleScripts': GOOGLE_SCRIPTS,
    'facebookScripts': FACEBOOK_SCRIPTS,
    'twitterScripts': TWITTER_SCRIPTS,
    'instagramScripts': INSTAGRAM_SCRIPTS,
    'otherScripts': OTHER_SCRIPTS,
    'biometricScripts': BIOMETRIC_SCRIPTS
}
with open('constants.yaml', 'w') as f:
    yaml.dump(constants, f, default_flow_style=False)

# Create output directory if necessary for output
if not (os.path.exists("output")):
    os.makedirs("output")
'''
else:  # Clean up output file by deleting anything in the folder, if it exists
    for file in os.listdir(OUT_PATH):
        os.remove(os.path.join(OUT_PATH, file))
'''
# Check which services are used and only load those access token
for service in access_config:
    print(access_config.get(service))
    if (access_config.get(service).get('used')):
        if service == 'google':
            if access_config.get(service).get('local'):
                # Google Takeout
                takout_files = glob.glob("takeout*.zip")
                for takeout_file in takout_files:
                    gTakeout = zipfile.ZipFile(os.path.join(PATH, takeout_file), 'r')
                    gTakeout.extractall(DATA_PATH)
        elif service == 'facebook':
            if access_config.get(service).get('local'):
                # Facebook zip
                facebook_zips = glob.glob("facebook*.zip")
                for facebook_zip in facebook_zips:
                    fbZip = zipfile.ZipFile(os.path.join(PATH, facebook_zip), 'r')
                    fbZip.extractall(os.path.join(DATA_PATH, "facebook"))
        elif service == 'linkedin':
            if access_config.get(service).get('local'):
                # LinkedIn zip
                linkedIn_zips = glob.glob("LinkedIn*.zip")
                for linkedIn_zip in linkedIn_zips:
                    linkedInZip = zipfile.ZipFile(os.path.join(PATH, linkedIn_zip), 'r')
                    linkedInZip.extractall(os.path.join(DATA_PATH, "linkedin"))

########################################################################################
#                        END BASIC SETUP                                               #
########################################################################################
'''
Execute the other scripts to create the database and fill it
'''

# Try creating database
exec(compile(open("databaseSetup.py", "rb").read(), "databaseSetup.py", 'exec'))

# execute on biometric data first
# Sleep
if access_config.get('local').get('biometric'):
    if access_config.get('local').get('sleep'):
        Bio_PATH = os.path.join(BIOMETRIC_SCRIPTS, "Fitness", "Sleep")
        for executables in os.listdir(os.path.join(Bio_PATH)):
            exec(compile(open(os.path.join(Bio_PATH, executables), "rb").read(),
                         os.path.join(Bio_PATH, executables), 'exec'))
    # Heart
    if access_config.get('local').get('heart'):
        Bio_PATH = os.path.join(BIOMETRIC_SCRIPTS, "Fitness", "Heart")
        for executables in os.listdir(os.path.join(Bio_PATH)):
            exec(compile(open(os.path.join(Bio_PATH, executables), "rb").read(),
                         os.path.join(Bio_PATH, executables), 'exec'))

    if access_config.get('local').get('weight'):
        Bio_PATH = os.path.join(BIOMETRIC_SCRIPTS, "Fitness", "Weight")
        for executables in os.listdir(os.path.join(Bio_PATH)):
            exec(compile(open(os.path.join(Bio_PATH, executables), "rb").read(),
                         os.path.join(Bio_PATH, executables), 'exec'))

    if access_config.get('local').get('hexoskin'):
        Bio_PATH = os.path.join(BIOMETRIC_SCRIPTS, "Sensors", "Hexoskin")
        for executables in os.listdir(os.path.join(Bio_PATH)):
            exec(compile(open(os.path.join(Bio_PATH, executables), "rb").read(),
                         os.path.join(Bio_PATH, executables), 'exec'))

    if access_config.get('local').get('reconjet'):
        Bio_PATH = os.path.join(BIOMETRIC_SCRIPTS, "Sensors", "ReconJet")
        for executables in os.listdir(os.path.join(Bio_PATH)):
            exec(compile(open(os.path.join(Bio_PATH, executables), "rb").read(),
                         os.path.join(Bio_PATH, executables), 'exec'))

    if access_config.get('local').get('myo'):
        Bio_PATH = os.path.join(BIOMETRIC_SCRIPTS, "Sensors", "Myo")
        for executables in os.listdir(os.path.join(Bio_PATH)):
            exec(compile(open(os.path.join(Bio_PATH, executables), "rb").read(),
                         os.path.join(Bio_PATH, executables), 'exec'))

# execute the ones that work on Google Takeout data first
if access_config.get('google').get('used'):
    google_count = 0
    if os.path.exists("progress.yaml"):
        with open("progress.yaml", "r") as progress_source:
            progress_dict = yaml.load(progress_source)
            google_count = progress_dict.get('googleProgress')
    for index, executables in enumerate(os.listdir(GOOGLE_SCRIPTS)):
        if index >= google_count:
            exec(compile(open(os.path.join(GOOGLE_SCRIPTS, executables), "rb").read(),
                         os.path.join(GOOGLE_SCRIPTS, executables), 'exec'))
            google_count += 1
            with open("progress.yaml", "w") as progress:
                yaml.dump({'googleProgress': google_count}, progress, default_flow_style=False)

# Then on other zipped files
if access_config.get('facebook').get('used'):
    for executables in os.listdir(FACEBOOK_SCRIPTS):
        exec(compile(open(os.path.join(FACEBOOK_SCRIPTS, executables), "rb").read(),
                     os.path.join(FACEBOOK_SCRIPTS, executables), 'exec'))

if access_config.get('linkedin').get('used'):
    exec(compile(open("LinkedIn2JSON.py", "rb").read()), "LinkedIn2JSON.py", 'exec')

if access_config.get('twitter').get('used'):
    for executables in os.listdir(TWITTER_SCRIPTS):
        exec(compile(open(os.path.join(TWITTER_SCRIPTS, executables), "rb").read(),
                     os.path.join(TWITTER_SCRIPTS, executables), 'exec'))

if access_config.get('flickr').get('used'):
    exec(compile(open("Flickr2SQLite.py", "rb").read()), "Flickr2SQLite.py", 'exec')

if access_config.get('instagram').get('used'):
    for executables in os.listdir(INSTAGRAM_SCRIPTS):
        exec(compile(open(os.path.join(INSTAGRAM_SCRIPTS, executables), "rb").read(),
                     os.path.join(INSTAGRAM_SCRIPTS, executables), 'exec'))

if access_config.get('local').get('used'):
    for executables in os.listdir(OTHER_SCRIPTS):
        exec(compile(open(os.path.join(OTHER_SCRIPTS, executables), "rb").read(),
                     os.path.join(OTHER_SCRIPTS, executables), 'exec'))
