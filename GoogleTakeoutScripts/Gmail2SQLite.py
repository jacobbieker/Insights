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
import os
import mailbox
import yaml
from databaseSetup import Message

# Have to do this because when the command is called from the import in any subfolder it cannot find the dbconfig
if __name__ == "__main__":
    with open(os.path.join("constants.yaml"), 'r') as ymlfile:
        constants = yaml.load(ymlfile)
else:
    with open("constants.yaml", 'r') as ymlfile:
        constants = yaml.load(ymlfile)

MBOX = os.path.join(constants.get('dataDir'), 'Takeout', 'Mail', 'All mail Including Spam and Trash.mbox')

def print_payload(message):
    # if the message is multipart, its payload is a list of messages
    if message.is_multipart():
        for part in message.get_payload():
            print_payload(part)
    else:
        Message.insert({'date': message.get('date'),
                        'type': 'email',
                        'sender': message.get('from'),
                        'reciever': message.get('to'),
                        'message': message.get_payload()}).execute()

print("Starting Google Mail Parsing")
mbox = mailbox.mbox(MBOX)
for message in mbox:
    print_payload(message)
