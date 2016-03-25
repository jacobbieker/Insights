import os
import mailbox
import email
import quopri
import json
import time
from bs4 import BeautifulSoup
from dateutil.parser import parse
import yaml

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
        print(message.get_payload(decode=True))

mbox = mailbox.mbox(MBOX)
for message in mbox:
    print(message['subject'])
    print_payload(message)