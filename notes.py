#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import traceback
from collections import OrderedDict
from peewee import *
import readline
import models as m
from utils import *

path = os.getenv('HOME', os.path.expanduser('~')) + '/.notes'
db = SqliteDatabase(path + '/diary.db')
m.proxy.initialize(db)
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
        db.create_tables([m.Note], safe=True)
    except DatabaseError as err:
        traceback.print_tb(err.__traceback__)
        exit(0)


def add_entry(data, title):
    m.Note.create(content=data, tags=None, title=title)


def add_entry_ui():
    """Add a note"""
    title_string = "Title (press {} when finished)".format(finish_key)
    print(title_string)
    print("=" * len(title_string))
    title = sys.stdin.read().strip()
    if title:
        entry_string = "\nEnter your entry: (press {} when finished)".format(finish_key)
        print(entry_string)
        data = sys.stdin.read().strip()
        if data:
            if input("\nSave entry (y/n) : ").lower() != 'n':
                add_entry(data, title)
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


def edit_entry(entry):
    clear_screen()
    title_string = "Title (press {} when finished)".format(finish_key)
    print(title_string)
    print("=" * len(title_string))
    readline.set_startup_hook(lambda: readline.insert_text(entry.title))
    try:
        title = sys.stdin.read().strip()
    finally:
        readline.set_startup_hook()
    if title:
        entry_string = "\nEnter your entry: (press {} when finished)".format(finish_key)
        print(entry_string)
        readline.set_startup_hook(lambda: readline.insert_text(entry.content))
        try:
            data = sys.stdin.read().strip()
        finally:
            readline.set_startup_hook()
        if data:
            if input("\nSave entry (y/n) : ").lower() != 'n':
                entry.title = title
                entry.content = data
                entry.save()
                return True
    else:
        print("No title entered! Press Enter to return to main menu")
        input()
        clear_screen()
        return False


def view_entry(entry):
    clear_screen()
    print(entry.title)
    print("=" * len(entry.title))
    print(entry.content)

    print('e) edit entry')
    print('d) delete entry')
    print('q) to return to view entries')

    next_action = input('Action: [e/d/q] : ').lower().strip()
    if next_action == 'd':
        return delete_entry(entry)
    elif next_action == 'e':
        return edit_entry(entry)
    elif next_action == 'q':
        return False


def view_entries():
    """View all the notes"""
    page_size = 2
    index = 0
    reset_flag = True

    while 1:
        clear_screen()
        if reset_flag:
            # Get entries if reset_flag is True
            # Will be True initially and on delete/edit entry
            entries = m.Note.select().order_by(m.Note.timestamp.desc())
            entries = list(entries)
            if not entries:
                print("Your search had no results. Press enter to return to the main menu!")
                input()
                clear_screen()
                return
            index = 0
            reset_flag = False
        paginated_entries = get_paginated_entries(entries, index, page_size)
        for i in range(len(paginated_entries)):
            entry = paginated_entries[i]
            timestamp = entry.timestamp.strftime("%A %B %d, %Y %I:%M%p")
            head = "\"{title}\" on \"{timestamp}\"".format(
                title=entry.title, timestamp=timestamp)
            print(str(i) + ") " + head)
        print('n) next page')
        print('p) previous page')
        print('q) to return to main menu')

        next_action = input('Action: [n/p/q] : ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'n':
            if index + page_size < len(entries):
                index += page_size
        elif next_action == 'p':
            if index - page_size >= 0:
                index -= page_size
        elif next_action.isdigit() and int(next_action) < len(paginated_entries) and int(next_action) >= 0:
            reset_flag = view_entry(paginated_entries[int(next_action)])


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
