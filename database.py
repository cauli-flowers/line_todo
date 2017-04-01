import peewee
from datetime import datetime, timedelta

db = peewee.SqliteDatabase('todo.db')


class Todo(peewee.Model):
    id = peewee.PrimaryKeyField()
    title = peewee.CharField()
    details = peewee.TextField()
    done = peewee.BooleanField()
    limit = peewee.DateTimeField()
    notification = peewee.DateTimeField()

    class Meta:
        database = db


def create_table():
    Todo.drop_table()

    Todo.create_table()

    Todo.create(
        id=1,
        title='sample1',
        details='details1',
        done=False,
        limit=datetime.now() + timedelta(days=1),
        notification=datetime.now() + timedelta(days=0.8),
    )