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
#import tcxparser
# import tcxparser
import os
from glob import glob

from insights.config.databaseSetup import Heart, Activity
from insights.io import config
# import tcxparser
# import tcxparser
import os
from glob import glob

from insights.config.databaseSetup import Heart, Activity
from insights.io import config

if __name__ != "__main__":
    configuration_files = config.import_yaml_files(".", ["constants"])
    constants = configuration_files[0]
else:
    configuration_files = config.import_yaml_files("..", ["constants"])
    constants = configuration_files[0]

rootdir = os.path.join(constants.get("dataDir"), "Takeout", "Fit")
tcx_files = [y for x in os.walk(rootdir) for y in glob(os.path.join(x[0], '*.tcx'))]
aggregation_files = [y for x in os.walk(rootdir) for y in glob(os.path.join(x[0], '*.csv'))]

###############################################################################################
#
#
#  This TCXParser taken from: https://github.com/vkurup/python-tcxparser
#
#
#################################################################################################
"Simple parser for Garmin TCX files."

import time
from lxml import objectify


namespace = 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'


class TCXParser:

    def __init__(self, tcx_file):
        tree = objectify.parse(tcx_file)
        self.root = tree.getroot()
        self.activity = self.root.Activities.Activity

    def hr_values(self):
        return [float(x.text) for x in self.root.xpath('//ns:HeartRateBpm/ns:Value', namespaces={'ns': namespace})]

    def altitude_points(self):
        return [float(x.text) for x in self.root.xpath('//ns:AltitudeMeters', namespaces={'ns': namespace})]

    @property
    def latitude(self):
        return self.activity.Lap.Track.Trackpoint.Position.LatitudeDegrees.pyval

    @property
    def longitude(self):
        return self.activity.Lap.Track.Trackpoint.Position.LongitudeDegrees.pyval

    @property
    def activity_type(self):
        return self.activity.attrib['Sport'].lower()

    @property
    def completed_at(self):
        return self.activity.Lap[-1].Track.Trackpoint[-1].Time.pyval

    @property
    def distance(self):
        return self.activity.Lap[-1].Track.Trackpoint[-2].DistanceMeters.pyval

    @property
    def distance_units(self):
        return 'meters'

    @property
    def duration(self):
        """Returns duration of workout in seconds."""
        return sum(lap.TotalTimeSeconds for lap in self.activity.Lap)

    @property
    def calories(self):
        return sum(lap.Calories for lap in self.activity.Lap)

    @property
    def hr_avg(self):
        """Average heart rate of the workout"""
        hr_data = self.hr_values()
        return sum(hr_data)/len(hr_data)

    @property
    def hr_max(self):
        """Minimum heart rate of the workout"""
        return max(self.hr_values())

    @property
    def hr_min(self):
        """Minimum heart rate of the workout"""
        return min(self.hr_values())

    @property
    def pace(self):
        """Average pace (mm:ss/km for the workout"""
        secs_per_km = self.duration/(self.distance/1000)
        return time.strftime('%M:%S', time.gmtime(secs_per_km))

    @property
    def altitude_avg(self):
        """Average altitude for the workout"""
        altitude_data = self.altitude_points()
        return sum(altitude_data)/len(altitude_data)

########################################################################################
#
# End of copied and slightly modified code
#
########################################################################################
print("Starting Google Fit Parsing")
for tcx_file in tcx_files:
    with open(os.path.join(rootdir, "Activities", tcx_file)) as activities:
        parsed = TCXParser(activities)
        if parsed.altitude_points():
            Activity.insert({'type': parsed.activity_type,
                             'duration': parsed.duration,
                             'end_time': parsed.completed_at,
                             'calories': parsed.calories,
                             'application': 'Google Fit',
                             'avg_altitude': parsed.altitude_avg,
                             }).execute()
        else:
            Activity.insert({'type': parsed.activity_type,
                             'duration': parsed.duration,
                             'end_time': parsed.completed_at,
                             'calories': parsed.calories,
                             'application': 'Google Fit',
                             }).execute()
        if parsed.hr_values():
            Heart.insert({'application': "Google Fit",
                          'duration': parsed.duration,
                          'end_time': parsed.completed_at,
                          'lowest': parsed.hr_min,
                          'highest': parsed.hr_max,
                          'average': parsed.hr_avg}).execute()
