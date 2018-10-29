# Demo file of tests
import notes
from notes import fn, add_entry, delete_entry, edit_entry, add_entry_ui, get_input
from peewee import *
import models as m
from crypto_utils import encrypt, key_to_store
import getpass
import unittest
import os
import mock

db_temp = SqliteDatabase(':memory:')

m.proxy.initialize(db_temp)
db_temp.connect()
db_temp.create_tables([m.Note], safe=True)


def test_add_entry():
    title = "avi"
    content = "How are you doing today?"
    password = "masterpassword"
    add_entry(content, title, password)
    entry = m.Note.get(m.Note.title == title)
    print(entry)
    assert entry.content == content

# sinput = ["Hello", "HelloWorld", "password"]
# i = ["y"] 

# def mock_stdin():
#     return sinput.pop(0)

# def mock_input():
#     return i[0]


# class TestRandom(unittest.TestCase):
#     @mock.patch('notes.get_input', side_effect=mock_stdin)
#     @mock.patch('getpass.getpass', side_effect=mock_stdin)
#     @mock.patch('notes.input', side_effect=mock_input)
#     def test_add_entry_ui_valid(self):
#         add_entry_ui()

# import unittest
# from os import urandom
# import mock


# def simple_urandom(length):
#     return 'f' * length


# class Testandom(unittest.TestCase):
#     @mock.patch('os.sys', side_effect=simple_urandom)
#     @mock.patch('os.getenv', side_effect=simple_urandom)
#     def test_urandom(self, urandom_function):
#         assert os.sys(5) == os.getenv(5)


    # notes.get_input = mock_stdin()

    # notes.input = mock_input

    # getpass.getpass = mock_stdin()

    # add_entry_ui() 


    # title_string = "Title (press {} when finished)".format(finish_key)
    # print(title_string)
    # print("=" * len(title_string))
    # title = sys.stdin.read().strip()
    # if title:
    #     entry_string = "\nEnter your entry: (press {} when finished)".format(finish_key)
    #     print(entry_string)
    #     data = sys.stdin.read().strip()
    #     if data:
    #         if input("\nSave entry (y/n) : ").lower() != 'n':
    #             while True:
    #                 password = getpass.getpass("Password To protect data: ")
    #                 if len(password) == 0:
    #                     print("Please input a valid password")
    #                 else:
    #                     break
    #             password_to_store = key_to_store(password)
    #             encryped_data = encrypt(data, password)
    #             add_entry(encryped_data, title, password_to_store)
    #             print("Saved successfully")
    # else:
    #     print("No title entered! Press Enter to return to main menu")
    #     input()
    #     clear_screen()
    #     return



def test_delete_entry():
    title = "yo"
    content = "Hello Lol"
    m.Note.create(content=content, tags=None, title=title)
    entry = m.Note.select().where(m.Note.title == title)
    if entry.exists():
        flag1 = 1
        entry = m.Note.get(m.Note.title == title)
    delete_entry(entry)
    entry = m.Note.select().where(m.Note.title == title)
    flag2 = 1
    if entry.exists():
        flag2 = 0
    assert flag1 == flag2


def test_edit_entry():
    title = "lost in this world"
    content = "Batman is forever lost!!!"
    password = "masterpassword"
    password_to_store = key_to_store(password)
    # Need to encrypt before storing
    m.Note.create(content=content, tags=None, title=title, password=password_to_store)
    entry = m.Note.get(m.Note.title == title)
    new_title = "Superhero Found"
    new_content = "Robin to the rescue!!!"
    encryped_data = encrypt(new_content, password)
    edit_entry(entry, new_title, new_content, password)
    entry = m.Note.select().where(m.Note.title == title)
    flag = 1
    if entry.exists():
        flag = 0
    entry = m.Note.get(m.Note.title == new_title)
    assert (entry.title, entry.content, entry.password, flag) == (new_title, encryped_data, password_to_store, 1)


'''def test_fn():
    assert fn(4) == 4**2'''

'''class Test(TestCase):
    def test_add_entry(self):
        with test_database(test_db, Note):
            title = "Hello World"
            content = "How are you doing today?"
            add_entry(content, title)
            entry = Note.get(Note.title == title)
            self.assertEqual(entry.content, content)'''




