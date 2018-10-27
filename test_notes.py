# Demo file of tests
from notes import fn, add_entry 
from peewee import *
import models as m

db_temp = SqliteDatabase(':memory:')

m.proxy.initialize(db_temp)


def test_add_entry():
	db_temp.connect()
	db_temp.create_tables([m.Note], safe=True)
	title = "aviral"
	content = "How are you doing today?"
	add_entry(content, title)
	entry = m.Note.get(m.Note.title == title)
	print(entry)
	assert entry.content == content


	
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




