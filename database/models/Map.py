from database import BaseModel
from database.models import Match, Team
from peewee import *

class Map(BaseModel):
    match_id = ForeignKeyField(Match, backref='maps')
    map_id = UUIDField(primary_key=True)
    map_num = SmallIntegerField()
    team1_score = SmallIntegerField()
    team2_score = SmallIntegerField()
    winner = ForeignKeyField(Team, backref='maps_won')
    map = TextField()
    team1_first_half_score = SmallIntegerField()
    team2_first_half_score = SmallIntegerField()
    team1_second_half_score = SmallIntegerField()
    team2_second_half_score = SmallIntegerField()
    team1_overtime_score = SmallIntegerField()
    team2_overtime_score = SmallIntegerField()
