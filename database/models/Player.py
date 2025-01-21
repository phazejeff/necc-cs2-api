from database import BaseModel
from database.models import Team
from peewee import *

class Player(BaseModel):
    player_id = TextField(primary_key=True)
    team = ForeignKeyField(Team, backref='players')
    nickname = TextField()
    avatar = TextField()
    level = SmallIntegerField()