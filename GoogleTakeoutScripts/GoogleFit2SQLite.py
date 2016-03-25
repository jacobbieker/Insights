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
import tcxparser
import os
import yaml
from glob import glob
from databaseSetup import Heart, Activity, Sleep

# Have to do this because when the command is called from the import in any subfolder it cannot find the dbconfig
if __name__ == "__main__":
    with open(os.path.join("constants.yaml"), 'r') as ymlfile:
        constants = yaml.load(ymlfile)
else:
    with open("constants.yaml", 'r') as ymlfile:
        constants = yaml.load(ymlfile)

rootdir = os.path.join(constants.get("dataDir"), "Takeout", "Fit")
tcx_files = [y for x in os.walk(rootdir) for y in glob(os.path.join(x[0], '*.tcx'))]
aggregation_files = [y for x in os.walk(rootdir) for y in glob(os.path.join(x[0], '*.csv'))]

for tcx_file in tcx_files:
    with open(os.path.join(rootdir, "Activities", tcx_file)) as activities:
        parsed = tcxparser.TCXParser(activities)
        Activity.create({'type': parsed.activity_type,
                         'duration': parsed.duration,
                         'end_time': parsed.completed_at,
                         'calories': parsed.calories,
                         'start_time': parsed.completed_at - parsed.duration,
                         'application': 'Google Fit',
                         'avg_altitude': parsed.altitude_avg,
                         'max_altitude': max(parsed.altitude_points()),
                         'min_altitude': min(parsed.altitude_points()),
                         }).insert()
        if parsed.hr_max != 0:
            Heart.create({'application': "Google Fit",
                          'duration': parsed.duration,
                          'start_time': parsed.completed_at - parsed.duration,
                          'end_time': parsed.completed_at,
                          'lowest': parsed.hr_min,
                          'highest': parsed.hr_max,
                          'average': parsed.hr_avg,
                          'activity': Activity.get({'end_time': parsed.completed_at})}).insert()
