# Demo file of tests
from peewee import *  # pylint: disable=redefined-builtin,wildcard-import
from notes import fn, add_entry, delete_entry, edit_entry
import models as m
from crypto_utils import encrypt, key_to_store

DB_TEMP = SqliteDatabase(':memory:')

m.proxy.initialize(DB_TEMP)
DB_TEMP.connect()
DB_TEMP.create_tables([m.Note], safe=True)


def test_add_entry():
    title = "avi"
    content = "How are you doing today?"
    password = "masterpassword"
    add_entry(content, title, password)
    entry = m.Note.get(m.Note.title == title)
    print(entry)
    assert entry.content == content


def test_delete_entry():
    title = "yo"
    content = "Hello Lol"
    m.Note.create(content=content, tags=None, title=title)
    entry = m.Note.select().where(m.Note.title == title)  # pylint: disable=assignment-from-no-return
    if entry.exists():
        flag1 = 1
        entry = m.Note.get(m.Note.title == title)  # pylint: disable=assignment-from-no-return
    delete_entry(entry)
    entry = m.Note.select().where(m.Note.title == title)  # pylint: disable=assignment-from-no-return
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
    assert (entry.title, entry.content, entry.password, flag) ==\
           (new_title, encryped_data, password_to_store, 1)
