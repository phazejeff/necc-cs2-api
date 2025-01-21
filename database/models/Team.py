from database import BaseModel
from peewee import *

class Team(BaseModel):
    team_id = TextField(primary_key=True)
    group = SmallIntegerField()
    name = TextField()
    avatar = TextField(null=True)