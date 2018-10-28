# Demo file of tests
from notes import fn, add_entry, delete_entry, edit_entry 
from peewee import *
import models as m
from crypto_utils import encrypt, key_to_store

db_temp = SqliteDatabase(':memory:')

m.proxy.initialize(db_temp)
db_temp.connect()
db_temp.create_tables([m.Note], safe=True)

def test_add_entry():
	title = "avi"
	content = "How are you doing today?"
	add_entry(content, title)
	entry = m.Note.get(m.Note.title == title)
	print(entry)
	assert entry.content == content

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




