from peewee import Model, SqliteDatabase

database = SqliteDatabase("2024Fall.db")

class BaseModel(Model):
    class Meta:
        database = database