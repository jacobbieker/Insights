'''
This file unzips downloaded files, gets data, and sets up file structure for use by the rest of the scripts
'''
__author__ = 'Jacob'
import os
import glob
import yaml
import zipfile

#read config data on database
with open("dbconfig.yaml", 'r') as ymlfile:
    config = yaml.load(ymlfile)
with open("access.yaml", 'r') as access:
    access_config = yaml.load(access)

#Constant current directory used by rest of the scripts:
PATH = os.curdir
OUT_PATH = PATH + "\output"
DATA_PATH = PATH + "\data"
DB_NAME = config['sqlite']['name'] + '.db'
GOOGLE_SCRIPTS = PATH + '\GoogleTakeoutScripts'


#Create config.yaml to be used for other scripts, so that they don't import setup.py
constants = {
    'path': PATH + '\\',
    'dataDir': DATA_PATH,
    'outputDir': OUT_PATH,
    'database': DB_NAME,
    'databaseLoc': PATH + '\\' + DB_NAME,
    'googleScripts': GOOGLE_SCRIPTS
}
with open('constants.yaml', 'w') as f:
  yaml.dump(constants, f, default_flow_style=False)

#Create output directory if necessary for output
if not (os.path.exists("output")):
    os.makedirs("output")
else: #Clean up output file by deleting anything in the folder, if it exists
    for file in os.listdir(OUT_PATH):
        os.remove(OUT_PATH + "\\" + file)

#TODO check each service and all if the service is used, in a generic way
'''
#Check which services are used and only load those access token
for service in access_config:
    if(service['used']):

'''
########################################################################################
#                        END BASIC SETUP                                               #
########################################################################################

# Unzip data archives for use in scripts
#Google Takout
takout_file = glob.glob("takout*.zip")
gTakeout = zipfile.ZipFile(PATH + "\\" + takout_file, 'r')
gTakeout.extractall(DATA_PATH)
#Facebook zip
facebook_zip = glob.glob("facebook*.zip")
fbZip = zipfile.ZipFile(PATH + "\\" + facebook_zip, 'r')
fbZip.extractall(DATA_PATH + "\\facebook\\")
#LinkedIn zip
linkedIn_zip = glob.glob("LinkedIn*.zip")
fbZip = zipfile.ZipFile(PATH + "\\" + linkedIn_zip, 'r')
fbZip.extractall(DATA_PATH + "\\linkedin\\")

'''
Execute the other scripts to create the database and fill it
'''
execfile("databaseSetup.py")
#execute the ones that work on Google Takeout data first
execfile(GOOGLE_SCRIPTS + "\\GVoice2JSON.py")
execfile(GOOGLE_SCRIPTS + "\\Gmail2JSON.py")
execfile(GOOGLE_SCRIPTS + "\\GmailJSON2SQLite.py")
execfile(GOOGLE_SCRIPTS + "\\Location2SQLite.py")

#Then on other zipped files
execfile("Facebook2JSON.py")
execfile("LinkedIn2JSON.py")

#Then on downloading data
execfile("Flickr2SQLite.py")
execfile("Twitter2SQLite.py")