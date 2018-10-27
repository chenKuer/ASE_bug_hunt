# Demo file of tests
from notes import fn, add_entry 
from models import Note


def test_fn():
    assert fn(4) == 4**2

def test_add_entry():
	title = "Hello World"
	content = "How are you doing today?"
	add_entry(content, title)
	entry = Note.get(Note.title == title)
	print(entry)
	assert entry.content == content

	




