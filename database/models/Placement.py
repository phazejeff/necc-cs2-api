from database import BaseModel
from database.models import Team
from peewee import *

class Placement(BaseModel):
    team_id = ForeignKeyField(Team)
    fall_season_placement = SmallIntegerField(default=0)
    fall_playoff_placement = SmallIntegerField(default=0)
    spring_season_placement = SmallIntegerField(default=0)
    spring_playoff_placement = SmallIntegerField(default=0)
    national_points = SmallIntegerField(default=0)