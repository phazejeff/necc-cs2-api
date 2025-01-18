from . import *
from peewee import *

class Team(BaseModel):
    team_id = TextField(primary_key=True)
    group = SmallIntegerField()
    captain = ForeignKeyField(Player)
    name = TextField()
    avatar = TextField()