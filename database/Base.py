from peewee import Model
from peewee import SqliteDatabase
import os
from dotenv import load_dotenv
load_dotenv()
DB_NAME = os.getenv("DB_NAME")

database = SqliteDatabase(DB_NAME)

class BaseModel(Model):
    class Meta:
        database = database