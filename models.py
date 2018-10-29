import datetime
import os

from peewee import *

path = os.getenv('HOME', os.path.expanduser('~')) + '/.notes'
#db = SqliteDatabase(path + '/diary.db')

proxy = Proxy()

class Note(Model):
    """
    Note model in db
    """
    title = CharField()
    content = TextField()
    password = TextField(null=True)
    timestamp = DateTimeField(default=datetime.datetime.now)
    tags = CharField(null=True)

    class Meta:
        database = proxy
