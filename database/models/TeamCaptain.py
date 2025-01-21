from database import BaseModel
from database.models import Player, Team
from peewee import *

class TeamCaptain(BaseModel):
    team_id = ForeignKeyField(Team)
    player_id = ForeignKeyField(Player)