# Demo file of tests
from notes import fn, add_entry, delete_entry 
from peewee import *
import models as m

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




