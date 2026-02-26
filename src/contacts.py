import json
import sys
import os

CONTACTS_FILE = "contacts.json" 

def load_contacts():
    ''' Read contact list from JSON file. If file does not exist, creates new one'''