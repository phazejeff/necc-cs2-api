from database import BaseModel
from database.models import Team
from peewee import *

class Match(BaseModel):
    match_id = TextField(primary_key=True)
    team1 = ForeignKeyField(Team, backref='matches_as_team1')
    team2 = ForeignKeyField(Team, backref='matches_as_team2')
    winner = ForeignKeyField(Team, backref='matches_won')
    url = TextField()
    finished_at = DateTimeField()
    week = SmallIntegerField()