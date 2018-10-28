#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import traceback
from collections import OrderedDict
from peewee import *

from models import Note
from utils import *
from encryption import *

import time

# Kept this function here to keep Travis builds passing till actual tests are added
def fn(x):
    return x ** 2


path = os.getenv('HOME', os.path.expanduser('~')) + '/.notes'
db = SqliteDatabase(path + '/diary.db')
finish_key = "ctrl+Z" if os.name == 'nt' else "ctrl+D"

def init():
    """
    Initialize and create database
    :return: void
    """
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        db.connect()
        db.create_tables([Note], safe=True)
    except DatabaseError as err:
        traceback.print_tb(err.__traceback__)
        exit(0)


def add_entry(data, title, password):
    Note.create(content=data, tags=None, title=title, password=password)


def add_entry_ui():
    """Add a note"""
    title_string = "Title (press {} when finished)".format(finish_key)
    print(title_string)
    print("="*len(title_string))
    title = sys.stdin.read().strip()
    if title:
        entry_string = "\nEnter your entry: (press {} when finished)".format(finish_key)
        print(entry_string)
        data = sys.stdin.read().strip()
        if data:
            if input("\nSave entry (y/n) : ").lower() != 'n':
                while True:
                    password = input("Input a password to protect the note: ")
                    if password == '':
                        print("Please input a valid password")
                    else:
                        break
                password_to_store = key_to_store(password)
                encryped_data = encrypt(data, password)
                add_entry(encryped_data, title, password_to_store)
                print("Saved successfully")
    else:
        print("No title entered! Press Enter to return to main menu")
        input()
        clear_screen()
        return


def menu_loop():
    """To display the diary menu"""
    choice = None
    while choice != 'q':
        clear_screen()
        print(path)
        banner = r"""
         _   _       _            
        | \ | |     | |           
        |  \| | ___ | |_ ___  ___ 
        | . ` |/ _ \| __/ _ \/ __|
        | |\  | (_) | ||  __/\__ \
        \_| \_/\___/ \__\___||___/
        """
        print(banner)
        print("Enter 'q' to quit")
        for key, value in MENU.items():
            print('{}) {} : '.format(key, value.__doc__))
        choice = input('Action : ').lower().strip()

        if choice in MENU:
            clear_screen()
            MENU[choice]()
    clear_screen()


def delete_entry(entry):
    return entry.delete_instance()


def view_entry(entry, password):
    clear_screen()

    print(entry.title)
    print("=" * len(entry.title))
    print(decrypt(entry.content, password))

    print('e) edit entry')
    print('d) delete entry')
    print('q) to return to view entries')

    next_action = input('Action: [e/d/q] : ').lower().strip()
    if next_action == 'd':
        delete_entry(entry)
    elif next_action == 'q':
        return


def view_entries():
    """View all the notes"""
    page_size = 2
    entries = Note.select().order_by(Note.timestamp.desc())
    entries = list(entries)
    if not entries:
        print("Your search had no results. Press enter to return to the main menu!")
        input()
        clear_screen()
        return

    index = 0

    while 1:
        clear_screen()
        paginated_entries = get_paginated_entries(entries, index, page_size)
        for i in range(len(paginated_entries)):
            entry = paginated_entries[i]
            timestamp = entry.timestamp.strftime("%A %B %d, %Y %I:%M%p")
            head = "\"{title}\" \"{password}\" \"{content}\" on \"{timestamp}\"".format(
                title=entry.title, password=entry.password, content= entry.content, timestamp=timestamp)
            print(str(i) + ") " + head)
        print('n) next page')
        print('p) previous page')
        print('q) to return to main menu')

        next_action = input('Action: [n/p/q] : ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'n':
            index += page_size
        elif next_action == 'p':
            index -= page_size
        elif next_action.isdigit() and int(next_action) < len(paginated_entries) and int(next_action) >= 0:
            #TODO Ask for password. Show Error or Display content.
            while 1:
                password = input("Input the password to retrieve the text: ")
                entry = paginated_entries[int(next_action)]
                if key_to_store(password) != entry.password:
                    if input("Password is incorrect. Do you want to retry? (y/n): ").lower() != 'y':
                        break
                else:
                    view_entry(paginated_entries[int(next_action)], password)
                    break


MENU = OrderedDict([
    ('a', add_entry_ui),
    ('v', view_entries)
])

if __name__ == "__main__":
    init()
    try:
        menu_loop()
    except KeyboardInterrupt:
        clear_screen()
        sys.exit(0)
