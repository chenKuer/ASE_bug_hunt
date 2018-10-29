import datetime
import os

from peewee import *  # pylint: disable=redefined-builtin,wildcard-import

PATH = os.getenv('HOME', os.path.expanduser('~')) + '/.notes'

proxy = Proxy()  # pylint: disable=invalid-name


class Note(Model):
    """
    Note model in db
    """
    title = CharField()
    content = TextField()
    password = TextField(null=True)
    timestamp = DateTimeField(default=datetime.datetime.now)
    tags = CharField(null=True)

    class Meta: # pylint: disable=too-few-public-methods
        database = proxy
