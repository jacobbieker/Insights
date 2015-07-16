# Insights
A set of Python and R scripts to organize and analyze data from various sources and formats and make that data
easy to access and manipulate.

# Dependencies
peewee >= 2.6.0, rawkit, readexif, python-instagram, tweepy, facebook, github3
Only tested on Python 2.7
https://github.com/jay0lee/got-your-back to access GMail data, at least until mbox can get made to work

# Use
To use these scripts, download your Facebook, LinkedIn, and Google Takeout archives, and unzip them to the data folder
Then run insights.py. Currently, many of the scripts take a long time to run, so it might be better to walk away from the
computer for awhile and let it run.

# Contributions
Fork and pull request away! Any help is appreciated.

# Known Issues
All the scripts that work with live data, such as Instagram, Facebook Graph API, etc. as of right now should only
authenticate and do nothing else.
In PhotoEXIF2YAML.py, RAW files still throw errors.
For other issues, look at the Issues tab.

# License
    
    Copyright (C) 2015  Jacob Bieker
    
    jacob@bieker.us, www.jacobbieker.com
 
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