from datetime import datetime
from peewee import *

db = SqliteDatabase("discord.db")


class TimestampTzField(Field):
    """
    A timestamp field that supports a timezone by serializing the value
    with isoformat.
    """

    field_type = "TEXT"  # This is how the field appears in Sqlite

    def db_value(self, value: datetime) -> str:
        print(value)
        print(type(value))
        if value:
            return value.isoformat()

    def python_value(self, value: str) -> str:
        if value:
            return datetime.fromisoformat(value)


class BaseModel(Model):
    class Meta:
        database = db
