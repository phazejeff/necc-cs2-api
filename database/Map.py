from . import *
from peewee import *

class Map(BaseModel):
    match_id = ForeignKeyField(Match)
    map_id = AutoField()
    map_num = SmallIntegerField()
    team1_score = SmallIntegerField()
    team2_score = SmallIntegerField()
    map = TextField()
    team1 = ForeignKeyField(Team)
    team2 = ForeignKeyField(Team)
    team1_first_half_score = SmallIntegerField()
    team2_first_half_score = SmallIntegerField()
    team1_second_half_score = SmallIntegerField()
    team2_second_half_score = SmallIntegerField()
    team1_overtime_score = SmallIntegerField()
    team2_overtime_score = SmallIntegerField()
