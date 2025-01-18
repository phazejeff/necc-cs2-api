from . import *
from peewee import *

class Player(BaseModel):
    player_id = TextField(primary_key=True)
    team = ForeignKeyField(Team)
    nickname = TextField()
    avatar = TextField()
    level = SmallIntegerField()