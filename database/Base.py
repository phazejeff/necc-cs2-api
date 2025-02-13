from peewee import Model
from peewee import SqliteDatabase
import os
from dotenv import load_dotenv
load_dotenv()
DB_NAME = os.getenv("DB_NAME")
path = os.path.realpath(__file__)
path = os.path.dirname(path)
path = os.path.dirname(path)
database = SqliteDatabase(os.path.join(path, 'static', DB_NAME))

class BaseModel(Model):
    class Meta:
        database = database