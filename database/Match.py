from . import *
from peewee import *

class Match(BaseModel):
    match_id = TextField(primary_key=True)
    team1 = ForeignKeyField(Team)
    team2 = ForeignKeyField(Team)
    map1 = ForeignKeyField(Map)
    map2 = ForeignKeyField(Map)
    map3 = ForeignKeyField(Map)
    url = TextField()
    finished_at = DateTimeField()
    schedules_at = DateTimeField()
    started_at = DateTimeField()
    week = SmallIntegerField()