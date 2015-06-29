__author__ = 'Jacob'
import csv
import os
import json

'''
with open("constants.yaml", 'r') as ymlfile:
    constants = yaml.load(ymlfile)
'''

rootdir = "C:\Users\jacob_000\OneDrive\Personal_Projects\LinkedIn"

for file in os.listdir(rootdir):
    if (file.endswith(".csv")):
        #TODO Use config file for this?
        if(file == "Organizations.csv" or file == "Honors.csv" or file == "Education.csv" or file == "Positions.csv" or
                   file == "Projects.csv" or file == "Courses.csv"):
            with open(rootdir + "\\" + file, 'r') as source:
                file_name = os.path.splitext(os.path.basename(file))
                csv_reader = csv.DictReader(x.replace('\0', '') for x in source)
                with open(os.path.join('C:\Development\personal_analysis\output', 'linkedin.' + file_name[0] + '.json'), 'a') as json_output:
                    for row in csv_reader:
                        json_data = row
                        #Output to file
                        json_array = json.dump(json_data, json_output, sort_keys=True, indent=4)